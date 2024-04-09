import requests
import datetime
import uuid
from dataclasses import dataclass, field
from typing import Optional

import apps.config


class APIBase:
    max_runs: int = 5
    api_endpoint: str = f'http://{apps.config.Config.API_ENDPOINT}:{apps.config.Config.API_PORT}'

    @staticmethod
    def datetime_from_str(datetime_str):
        return datetime.datetime.strptime(datetime_str.split('+')[0], '%Y-%m-%d %H:%M:%S.%f')


@dataclass
class StepRun(APIBase):
    step_run_id: uuid.UUID
    step_id: uuid.UUID
    transaction_run_id: uuid.UUID
    run_start: datetime.datetime
    run_end: datetime.datetime
    run_result: str
    log_id: uuid.UUID
    screenshot_id: uuid.UUID
    error_code: Optional[int]

    transaction_id: Optional[uuid.UUID] = field(default=None, init=False)
    transaction_name: Optional[str] = field(default=None, init=False)
    step_name: Optional[str] = field(default=None, init=False)

    @staticmethod
    def from_json(json):
        return StepRun(
            step_run_id=uuid.UUID(json['steprunid']),
            step_id=uuid.UUID(json['stepid']),
            transaction_run_id=uuid.UUID(json['transactionrunid']),
            run_start=APIBase.datetime_from_str(json['runstart']),
            run_end=APIBase.datetime_from_str(json['runend']),
            run_result=json['runresult'],
            log_id=uuid.UUID(json['logid']),
            screenshot_id=uuid.UUID(json['screenshotid']),
            error_code=json['errorcode']
        )


@dataclass
class Step(APIBase):
    step_id: uuid.UUID
    transaction_id: uuid.UUID
    name: str
    description: str
    created_datetime: datetime.datetime
    created_by: str

    transaction_name: Optional[str] = field(default=None, init=False)
    runs: Optional[list] = field(default=None, init=False)

    @staticmethod
    def from_id(step_id):
        try:
            url = f'{APIBase.api_endpoint}/steps/{step_id}'
            response = requests.get(url)
            subresult = response.json()['steps'][0]

            result = Step.from_json(subresult)
            transaction = Transaction.from_id(result.transaction_id)
            result.transaction_name = transaction.name

            return result
        except Exception as e:
            print(f"[ERR] Can't init step from id: {e}")
            return None

    @staticmethod
    def from_json(json):
        return Step(
            step_id=uuid.UUID(json['stepid']),
            transaction_id=uuid.UUID(json['transactionid']),
            name=json['name'],
            description=json['description'],
            created_datetime=APIBase.datetime_from_str(json['createddatetime']),
            created_by=json['createdby']
        )

    def get_runs(self, run_result=None, max_runs=APIBase.max_runs):
        try:
            url = f'{self.api_endpoint}/steps/{self.step_id}/runs' + \
                  (f'?first={max_runs}' if run_result is None else f'/filter?key=runresult&value={run_result}&first={max_runs}')
            response = requests.get(url)
            self.runs = []
            for run in response.json()['step_runs']:
                step_run = StepRun.from_json(run)
                step_run.transaction_name = self.transaction_name
                step_run.transaction_id = self.transaction_id
                step_run.step_name = self.name
                self.runs.append(step_run)

            return self.runs
        except Exception as e:
            print(f"[ERR] Can't get runs for step {self.step_id}: {e}")
            return []


@dataclass
class TransactionRun(APIBase):
    transaction_run_id: uuid.UUID
    transaction_id: uuid.UUID
    robot_id: str
    run_start: datetime.datetime
    run_end: datetime.datetime
    run_result: str
    log_id: Optional[uuid.UUID]
    error_code: Optional[int]

    name: Optional[str] = field(default=None, init=False)
    steps: Optional[list] = field(default=None, init=False)

    @staticmethod
    def from_id(transaction_run_id):
        try:
            url = f'{APIBase.api_endpoint}/runs/{transaction_run_id}'
            response = requests.get(url)
            subresult = response.json()['runs'][0]

            result = TransactionRun.from_json(subresult)
            transaction = Transaction.from_id(result.transaction_id)
            result.name = transaction.name

            return result
        except Exception as e:
            print(f"[ERR] Can't init transaction run from id: {e}")
            return None

    @staticmethod
    def from_json(json):
        return TransactionRun(
            transaction_run_id=uuid.UUID(json['transactionrunid']),
            transaction_id=uuid.UUID(json['transactionid']),
            robot_id=json['robotid'],
            run_start=APIBase.datetime_from_str(json['runstart']),
            run_end=APIBase.datetime_from_str(json['runend']),
            run_result=json['runresult'],
            log_id=uuid.UUID(json['logid']) if json['logid'] else None,
            error_code=json['errorcode']
        )

    def get_steps(self):
        try:
            url = f'{self.api_endpoint}/runs/{self.transaction_run_id}/steps'
            response = requests.get(url)
            self.steps = []
            for run in response.json()['step_runs']:
                step_run = StepRun.from_json(run)
                step_run.step_name = Step.from_id(step_run.step_id).name
                step_run.transaction_name = self.name
                step_run.transaction_id = self.transaction_id
                self.steps.append(step_run)

            return self.steps
        except Exception as e:
            print(f"[ERR] Can't get steps for transaction run {self.transaction_run_id}: {e}")
            return []


@dataclass
class Transaction(APIBase):
    transaction_id: uuid.UUID
    name: str
    process_id: Optional[uuid.UUID]
    description: str
    created_datetime: datetime.datetime
    created_by: str
    state: str
    cron: str

    runs: Optional[list] = field(default=None, init=False)
    steps: Optional[list] = field(default=None, init=False)
    steps_count: Optional[int] = field(default=None, init=False)
    process: Optional[str] = field(default=None, init=False)

    @staticmethod
    def from_id(transaction_id):
        try:
            url = f'{APIBase.api_endpoint}/transactions/{transaction_id}'
            response = requests.get(url)
            subresult = response.json()['transactions'][0]

            result = Transaction.from_json(subresult)
            process = BusinessProcess.from_id(result.process_id)
            result.process = process.name

            return result
        except Exception as e:
            print(f"[ERR] Can't init transaction from id: {e}")
            return None

    @staticmethod
    def from_json(json):
        return Transaction(
            transaction_id=uuid.UUID(json['transactionid']),
            name=json['name'],
            process_id=uuid.UUID(json['processid']) if json['processid'] else None,
            description=json['description'],
            created_datetime=APIBase.datetime_from_str(json['createddatetime']),
            created_by=json['createdby'],
            state=json['state'],
            cron=json['cron']
        )

    def get_steps(self):
        try:
            url = f'{self.api_endpoint}/transactions/{self.transaction_id}/steps'
            response = requests.get(url)
            self.steps = []
            for step in response.json()['steps']:
                transaction_step = Step.from_json(step)
                transaction_step.transaction_name = self.name
                # we don't need to get runs for each step
                self.steps.append(transaction_step)

            self.steps_count = len(self.steps)
            return self.steps

        except Exception as e:
            print(f"[ERR] Can't get steps for transaction {self.transaction_id}: {e}")
            return []

    def get_runs(self, result=None, max_runs=APIBase.max_runs):
        try:
            url = f'{self.api_endpoint}/transactions/{self.transaction_id}/runs' + \
                  (f'?first={max_runs}' if result is None else f'/filter?key=runresult&value={result}&first={max_runs}')
            response = requests.get(url)
            self.runs = []
            for run in response.json()['runs']:
                transaction_run = TransactionRun.from_json(run)
                transaction_run.name = self.name
                # we don't need to get steps for each run
                self.runs.append(transaction_run)

            return self.runs
        except Exception as e:
            print(f"[ERR] Can't get runs for transaction {self.transaction_id}: {e}")
            return []


@dataclass
class BusinessProcess(APIBase):
    process_id: uuid.UUID
    name: str
    description: str
    created_datetime: datetime.datetime
    created_by: str

    transactions: Optional[list] = field(default=None, init=False)
    transactions_count: Optional[int] = field(default=None, init=False)
    sla_history: Optional[list] = field(default=None, init=False)
    service: Optional[str] = field(default=None, init=False)


    @staticmethod
    def add(name, description, created_by):
        try:
            url = f'{APIBase.api_endpoint}/processes'
            json_data = {
                "processes": [
                    {
                        "name": name,
                        "description": description,
                        "createdby": created_by
                    }
                ]
            }

            headers = {
                "Content-Type": "application/json"
            }

            response = requests.post(url, json=json_data, headers=headers)
            result = response.json()

            print(f"[DBG][BusinessProcess/add] response: {response}")

            return result
        except Exception as e:
            print(f"[ERR] Can't add process from id: {e}")
            return None


    @staticmethod
    def delete(process_id):
        try:
            url = f'{APIBase.api_endpoint}/processes/{process_id}'

            headers = {
                "Accept": "application/json"
            }

            response = requests.delete(url, headers=headers)
            result = response.json()

            print(f"[DBG][BusinessProcess/delete] response: {response}")

            return result
        except Exception as e:
            print(f"[ERR] Can't delete process id: {e}")
            return None


    @staticmethod
    def from_id(process_id):
        try:
            url = f'{APIBase.api_endpoint}/business_processes/{process_id}'
            response = requests.get(url)
            subresult = response.json()['business_processes'][0]

            result = BusinessProcess.from_json(subresult)
            service = Service.from_id(result.service_id)
            result.service = service.name

            return result

        except Exception as e:
            print(f"[ERR] Can't init process from id: {e}")
            return None

    @staticmethod
    def from_json(json):
        return BusinessProcess(
            process_id=uuid.UUID(json['processid']),
            name=json['name'],
            description=json['description'],
            created_datetime=APIBase.datetime_from_str(json['createddatetime']),
            created_by=json['createdby'],
        )

    def get_transactions(self):
        try:
            url = f'{self.api_endpoint}/business_processes/{self.process_id}/transactions'
            response = requests.get(url)
            raw_transactions = response.json()['transactions']
            self.transactions_count = len(raw_transactions)

            self.transactions = []
            self.sla_history = [0 for _ in range(APIBase.max_runs)]
            for transaction in raw_transactions:
                transaction_obj = Transaction.from_json(transaction)
                transaction_obj.get_runs()
                for i in range(APIBase.max_runs):
                    self.sla_history[i] += int(transaction_obj.runs[i].run_result == 'OK')
                self.transactions.append(transaction_obj)

            for i in range(APIBase.max_runs):
                self.sla_history[i] /= self.transactions_count
                self.sla_history[i] *= 100

            return self.transactions
        except Exception as e:
            print(f"[ERR] Can't get transactions for process {self.process_id}: {e}")
            return []


@dataclass
class Service(APIBase):
    service_id: uuid.UUID
    name: str
    description: str
    created_datetime: datetime.datetime
    created_by: str

    processes: Optional[list] = field(default=None, init=False)
    processes_count: Optional[int] = field(default=None, init=False)

    @staticmethod
    def from_id(service_id):
        try:
            url = f'{APIBase.api_endpoint}/services/{service_id}'
            response = requests.get(url)
            subresult = response.json()['services'][0]

            result = Service.from_json(subresult)

            return result
        except Exception as e:
            print(f"[ERR] Can't init service from id: {e}")
            return None

    @staticmethod
    def from_json(json):
        return Service(
            service_id=uuid.UUID(json['serviceid']),
            name=json['name'],
            description=json['description'],
            created_datetime=APIBase.datetime_from_str(json['createddatetime']),
            created_by=json['createdby']
        )

    def get_processes(self):
        try:
            url = f'{self.api_endpoint}/services/{self.service_id}/business_processes'
            response = requests.get(url)
            self.processes = []
            for process in response.json()['business_processes']:
                process_obj = BusinessProcess.from_json(process)
                process_obj.get_transactions()
                self.processes.append(process_obj)

            return self.processes
        except Exception as e:
            print(f"[ERR] Can't get processes for service {self.service_id}: {e}")
            return []


# robots are separated from the rest of the entities
@dataclass
class Robot(APIBase):
    robot_id: str
    name: str
    city: str
    latitude: float
    longitude: float
    ip_address: str
    created_datetime: datetime.datetime
    created_by: str

    runs: Optional[list] = field(default=None, init=False)

    @staticmethod
    def from_id(robot_id):
        try:
            url = f'{APIBase.api_endpoint}/robots/{robot_id}'
            response = requests.get(url)
            subresult = response.json()['robots'][0]

            result = Robot.from_json(subresult)

            return result
        except Exception as e:
            print(f"[ERR] Can't init robot from id: {e}")
            return None

    @staticmethod
    def from_json(json):
        return Robot(
            robot_id=json['robotid'],
            name=json['name'],
            city=json['city'],
            latitude=json['latitude'],
            longitude=json['longitude'],
            ip_address=json['ipaddr'],
            created_datetime=APIBase.datetime_from_str(json['createddatetime']),
            created_by=json['createdby']
        )

    def get_runs(self, max_runs=APIBase.max_runs):
        try:
            url = f'{self.api_endpoint}/runs/filter?key=robotid&value={self.robot_id}&first={max_runs}'
            response = requests.get(url)
            self.runs = []
            for run in response.json()['transactions_runs']:
                transaction_run = TransactionRun.from_json(run)
                transaction_run.name = self.name
                self.runs.append(transaction_run)

            return self.runs
        except Exception as e:
            print(f"[ERR] Can't get runs for robot {self.robot_id}: {e}")
            return []

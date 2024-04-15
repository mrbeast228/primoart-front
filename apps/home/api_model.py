import requests
import datetime
import uuid
from dataclasses import dataclass, field
from typing import Optional
import json

import apps.config


class APIBase:
    max_runs: int = 5
    sla_target: float = 99.9
    api_endpoint: str = f'{apps.config.Config.API_ENDPOINT}'

    @staticmethod
    def datetime_from_str(datetime_str):
        return datetime.datetime.strptime(datetime_str.split('+')[0], '%Y-%m-%d %H:%M:%S.%f')
    
    @staticmethod
    def datetime_to_str(datetime_obj):
        if isinstance(datetime_obj, str):
            return datetime_obj
        elif isinstance(datetime_obj, datetime.datetime):
            return datetime_obj.strftime('%Y-%m-%d %H:%M:%S')
        else:
            raise ValueError("Invalid datetime!")


@dataclass
class GlobalSLA(APIBase):
    fail_cur: int
    sla_cur: float
    sla_prev: float
    sla_daily: float

    @staticmethod
    def from_json(json):
        return GlobalSLA(
            fail_cur=json['fail_cur'],
            sla_cur=json['sla_cur'],
            sla_prev=json['sla_prev'],
            sla_daily=json['sla_daily']
        )

    @staticmethod
    def from_api(start=None, end=None):
        try:
            url = f'{APIBase.api_endpoint}/global_sla'
            params = {}
            if start and end:
                params["start"] = APIBase.datetime_to_str(start)
                params["end"] = APIBase.datetime_to_str(end)
            response = requests.get(url, json=params)
            subresult = response.json()['global_sla']

            return GlobalSLA.from_json(subresult)
        except Exception as e:
            print(f"[ERR] Can't get global SLA: {e}")
            return {'fail_cur': 0, 'sla_cur': 0, 'sla_prev': 0, 'sla_daily': 0}


@dataclass
class StepRun(APIBase):
    step_run_id: uuid.UUID
    step_id: uuid.UUID
    transaction_run_id: uuid.UUID
    run_start: datetime.datetime
    run_end: datetime.datetime
    run_result: str
    log_id: uuid.UUID | None
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
            log_id=uuid.UUID(json['logid']) if 'logid' in json else None,
            screenshot_id=uuid.UUID(json['screenshotid']) if 'screenshotid' in json else None,
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
            subresult = response.json()['step'][0]

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
                  (
                      f'?first={max_runs}' if run_result is None else f'/filter?key=runresult&value={run_result}&first={max_runs}')
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
            subresult = response.json()['run']

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
            log_id=uuid.UUID(json['logid']) if 'logid' in json else None,
            error_code=json['errorcode']
        )

    @staticmethod
    def list_all(params=None):
        if params is None:
            params = {}
        try:
            url = f'{APIBase.api_endpoint}/runs'
            response = requests.get(url=url, json=params)
            subresult = response.json()['runs']

            return subresult
        except Exception as e:
            print(f"[ERR] Can't list transactions runs: {e}")
            return None

    def get_steps(self):
        try:
            url = f'{self.api_endpoint}/step_runs'
            response = requests.get(url, json={
                "transactionrunid": str(self.transaction_run_id),
            })
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
    service_id: Optional[uuid.UUID]
    description: str
    created_datetime: datetime.datetime
    created_by: str
    state: str
    cron: str

    runs: Optional[list] = field(default=None, init=False)
    steps_count: Optional[int] = field(default=None, init=False)
    process: Optional[str] = field(default=None, init=False)
    current_state: Optional[str] = field(default=None, init=False)

    # dynamic fields
    robots: Optional[dict]
    fail_cur: Optional[float]
    sla_cur: Optional[float]
    sla_prev: Optional[float]
    sla_daily: Optional[float]
    steps: Optional[dict]

    @staticmethod
    def from_id(transaction_id, sublists=False, start_time=None, end_time=None):
        try:
            url = f'{APIBase.api_endpoint}/transactions/{transaction_id}'
            params = {
                "sublists": sublists,
            }
            if start_time and end_time:
                params["start"] = APIBase.datetime_to_str(start_time)
                params["end"] = APIBase.datetime_to_str(end_time)
            response = requests.get(url, json=params)
            subresult = response.json()['transaction']

            result = Transaction.from_json(subresult)
            #service = Service.from_id(result.service_id)
            #result.service = service.name

            return result
        except Exception as e:
            print(f"[ERR] Can't init transaction from id: {e}")
            return None

    @staticmethod
    def from_json(json):
        return Transaction(
            transaction_id=uuid.UUID(json['transactionid']),
            name=json['name'],
            service_id=json['serviceid'],
            description=json['description'],
            created_datetime=APIBase.datetime_from_str(json['createddatetime']),
            created_by=json['createdby'],
            state=json['state'],
            cron=json['cron'],
            fail_cur=json['fail_cur'] if 'fail_cur' in json else None,
            sla_cur=json['sla_cur'] if 'sla_cur' in json else None,
            sla_prev=json['sla_prev'] if 'sla_prev' in json else None,
            sla_daily=json['sla_daily'] if 'sla_daily' in json else None,
            steps=json['steps'] if 'steps' in json else None,
            robots=json['robots'] if 'robots' in json else None
        )

    @staticmethod
    def list_all(params=None):
        if params is None:
            params = {}
        try:
            url = f'{APIBase.api_endpoint}/transactions'
            response = requests.get(url=url, json=params)
            subresult = response.json()['transactions']

            return subresult
        except Exception as e:
            print(f"[ERR] Can't list transactions: {e}")
            return None

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
    project_id: uuid.UUID
    name: str
    description: str
    created_datetime: datetime.datetime
    created_by: str

    transactions: Optional[list] = field(default=None, init=False)
    transactions_count: Optional[int] = field(default=None, init=False)
    sla_history: Optional[list] = field(default=None, init=False)
    service: Optional[str] = field(default=None, init=False)
    current_state: Optional[str] = field(default=None, init=False)

    # dynamic fields
    fail_cur: Optional[float]
    sla_cur: Optional[float]
    sla_prev: Optional[float]
    sla_daily: Optional[float]
    trans_daily: Optional[dict]
    services: Optional[dict]

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
    def edit(process_id, name, description, created_by):
        try:
            url = f'{APIBase.api_endpoint}/processes/{process_id}'
            json_data = {
                "process_patch":
                    {
                        "name": name,
                        "description": description,
                        "createdby": created_by
                    }
            }

            headers = {
                "Content-Type": "application/json",
                "Accept": "application/json"
            }

            print(f"[DBG][BusinessProcess/edit] json_data: {json_data}")

            response = requests.put(url, json=json_data, headers=headers)
            result = response.json()

            print(f"[DBG][BusinessProcess/edit] response: {response}")

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
    def from_id(process_id, sublists=False, start_time=None, end_time=None):

        #print(f"[DBG][BusinessProcess/from_id] process_id: {process_id}")

        try:
            url = f'{APIBase.api_endpoint}/processes/{process_id}'
            params = {
                "sublists": sublists,
            }
            if start_time and end_time:
                params["start"] = APIBase.datetime_to_str(start_time)
                params["end"] = APIBase.datetime_to_str(end_time)
            #print(f"[DBG][BusinessProcess/from_id] url: {url}")

            response = requests.get(url, json=params)

            subresult = response.json()
            #print(f"[DBG][BusinessProcess/from_id] subresult: {subresult}")

            result = BusinessProcess.from_json(subresult["process"])
            #print(f"[DBG][BusinessProcess/from_id] result: {result}")

            return result

        except Exception as e:
            print(f"[ERR] Can't init process from id: {e}")
            return None

    @staticmethod
    def from_json(json):
        #print(f"[DBG][BusinessProcess/from_json] json: {json}")

        return BusinessProcess(
            process_id=json['processid'] if 'processid' in json else json['pojectid'],
            project_id=json['projectid'] if 'projectid' in json else json['processid'], # alias hook
            name=json['name'],
            description=json['description'],
            created_datetime=json['createddatetime'],
            created_by=json['createdby'],
            fail_cur=json['fail_cur'] if 'fail_cur' in json else None,
            sla_cur=json['sla_cur'] if 'sla_cur' in json else None,
            sla_prev=json['sla_prev'] if 'sla_prev' in json else None,
            sla_daily=json['sla_daily'] if 'sla_daily' in json else None,
            trans_daily=json['trans_daily'] if 'trans_daily' in json else None,
            services=json['services'] if 'services' in json else None
        )


@dataclass
class Service(APIBase):
    service_id: uuid.UUID
    name: str
    description: str
    created_datetime: datetime.datetime
    created_by: str

    processes: Optional[list] = field(default=None, init=False)
    processes_count: Optional[int] = field(default=None, init=False)
    current_state: Optional[str] = field(default=None, init=False)

    # dynamic fields
    fail_cur: Optional[float]
    sla_cur: Optional[float]
    sla_prev: Optional[float]
    sla_daily: Optional[float]
    trans_ok: Optional[int]
    trans_warning: Optional[int]
    trans_fail: Optional[int]
    trans_daily: Optional[dict]
    transactions: Optional[dict]

    @staticmethod
    def add(project_id, name, description, created_by):
        try:
            url = f'{APIBase.api_endpoint}/services'
            json_data = {
                "services": [
                    {
                        "processid": project_id,
                        "name": name,
                        "description": description,
                        "createdby": created_by,
                        "state": "active"
                    }
                ]
            }

            headers = {
                "Content-Type": "application/json"
            }

            response = requests.post(url, json=json_data, headers=headers)
            result = response.json()

            print(f"[DBG][Service/add] response: {response}")

            return result
        except Exception as e:
            print(f"[ERR] Can't add service: {e}")
            return None

    @staticmethod
    def edit(service_id, project_id, name, description, created_by):
        try:
            url = f'{APIBase.api_endpoint}/services/{service_id}'
            json_data = {
                "service_patch":
                    {
                        "processid": project_id,
                        "name": name,
                        "description": description,
                        "createdby": created_by,
                        "state": "active"
                    }
            }

            headers = {
                "Content-Type": "application/json",
                "Accept": "application/json"
            }

            print(f"[DBG][Service/edit] json_data: {json_data}")

            response = requests.put(url, json=json_data, headers=headers)
            result = response.json()

            print(f"[DBG][Service/edit] response: {response}")

            return result
        except Exception as e:
            print(f"[ERR] Can't edit service: {e}")
            return None

    @staticmethod
    def delete(service_id):
        try:
            url = f'{APIBase.api_endpoint}/services/{service_id}'

            headers = {
                "Accept": "application/json"
            }

            response = requests.delete(url, headers=headers)
            result = response.json()

            print(f"[DBG][Service/delete] response: {response}")

            return result
        except Exception as e:
            print(f"[ERR] Can't delete service id: {e}")
            return None


    @staticmethod
    def from_id(service_id, sublists=False, start_time=None, end_time=None):
        try:
            url = f'{APIBase.api_endpoint}/services/{service_id}'
            params = {
                "sublists": sublists,
            }
            if start_time and end_time:
                params["start"] = APIBase.datetime_to_str(start_time)
                params["end"] = APIBase.datetime_to_str(end_time)
            response = requests.get(url, json=params)
            subresult = response.json()['service']

            result = Service.from_json(subresult)

            return result
        except Exception as e:
            print(f"[ERR] Can't init service from id: {e}")
            return None

    @staticmethod
    def from_json(json):
        #print(f"[DBG][Service/from_json] json: {json}")

        return Service(
            service_id=uuid.UUID(json['serviceid']),
            name=json['name'],
            description=json['description'],
            created_datetime=APIBase.datetime_from_str(json['createddatetime']),
            created_by=json['createdby'],
            fail_cur=json['fail_cur'] if 'fail_cur' in json else None,
            sla_cur=json['sla_cur'] if 'sla_cur' in json else None,
            sla_prev=json['sla_prev'] if 'sla_prev' in json else None,
            sla_daily=json['sla_daily'] if 'sla_daily' in json else None,
            trans_ok=json['trans_ok'] if 'trans_ok' in json else None,
            trans_warning=json['trans_warning'] if 'trans_warning' in json else None,
            trans_fail=json['trans_fail'] if 'trans_fail' in json else None,
            trans_daily=json['trans_daily'] if 'trans_daily' in json else None,
            transactions=json['transactions'] if 'transactions' in json else None
        )

    @staticmethod
    def list_all(filter_json={}):
        try:
            url = f'{APIBase.api_endpoint}/services'
            response = requests.get(url, json=filter_json)
            subresult = response.json()['services']

            return subresult
        except Exception as e:
            print(f"[ERR] Can't list services: {e}")
            return None


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
    stats: Optional[dict[str, float]] = field(default=None, init=False)
    current_state: Optional[str] = field(default=None, init=False)

    # dynamic fields
    fail_cur: Optional[int]
    sla_cur: Optional[float]
    sla_prev: Optional[float]
    sla_daily: Optional[float]

    @staticmethod
    def from_id(robot_id, start_time=None, end_time=None):
        try:
            url = f'{APIBase.api_endpoint}/robots/{robot_id}'
            params = {}
            if start_time and end_time:
                params["start"] = APIBase.datetime_to_str(start_time)
                params["end"] = APIBase.datetime_to_str(end_time)
            response = requests.get(url, json=params)
            subresult = response.json()['robot']

            result = Robot.from_json(subresult)

            return result
        except Exception as e:
            print(f"[ERR] Can't init robot from id: {e}")
            return None

    @staticmethod
    def extended_json(robot_id, start_time=None, end_time=None):
        try:
            url = f'{APIBase.api_endpoint}/robots/{robot_id}'
            params = {
                "sublists": True,
            }
            if start_time and end_time:
                params["start"] = APIBase.datetime_to_str(start_time)
                params["end"] = APIBase.datetime_to_str(end_time)
            response = requests.get(url, json=params)
            subresult = response.json()['robot']

            return subresult
        except Exception as e:
            print(f"[ERR] Can't get robot from id: {e}")
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
            created_by=json['createdby'],
            fail_cur=json['fail_cur'] if 'fail_cur' in json else None,
            sla_cur=json['sla_cur'] if 'sla_cur' in json else None,
            sla_prev=json['sla_prev'] if 'sla_prev' in json else None,
            sla_daily=json['sla_daily'] if 'sla_daily' in json else None
        )

    def get_runs(self, max_runs=APIBase.max_runs):
        try:
            url = f'{self.api_endpoint}/runs'
            response = requests.get(url, json={
                "robotid": self.robot_id,
                "page": 1,
                "per_page": max_runs
            })
            self.runs = []
            for run in response.json()['runs']:
                transaction_run = TransactionRun.from_json(run)
                transaction_run.name = self.name
                self.runs.append(transaction_run)

            return self.runs
        except Exception as e:
            print(f"[ERR] Can't get runs for robot {self.robot_id}: {e}")
            return []


class Charts(APIBase):
    @staticmethod
    def get_heatmap(filter_json):
        try:
            url = f'{APIBase.api_endpoint}/runs/heatmap'
            response = requests.get(url, json=filter_json)
            return response.json()['heatmap']
        except Exception as e:
            print(f"[ERR] Can't get heatmap data: {e}")
            return None

    @staticmethod
    def get_transaction_runs(service_id=None, robot_id=None, start_time="", end_time=""):
        try:
            config = {}
            if service_id:
                config["serviceid"] = service_id
            elif robot_id:
                config["robotid"] = robot_id

            transactions = Transaction.list_all(params=config)
            transactions_id = [tr["transactionid"] for tr in transactions]

            config = {
                "transactionid": transactions_id,
                "start": start_time,
                "end": end_time
            }
            runs = TransactionRun.list_all(params=config)

            return runs
        except Exception as e:
            print(f"[ERR] Can't get transaction runs data: {e}")
            return None

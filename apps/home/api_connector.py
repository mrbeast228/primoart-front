import io
import requests

import apps.home.api_model as api_model


class APIConnector(api_model.APIBase):
    last_loaded_robots = {}
    last_loaded_services = {}
    last_loaded_business_processes = {}
    last_loaded_transactions = {}
    paging_enabled = False # TODO: Implement pagination

    @classmethod
    def get_page(cls, lst, page=1, per_page=10):
        if not cls.paging_enabled or page < 1:
            return lst
        start = (page - 1) * per_page
        end = start + per_page
        return lst[start:end]

    @classmethod
    def get_robots_list(cls, full=True, page=1, per_page=10):
        try:
            url = f'{cls.api_endpoint}/robots'
            response = requests.get(url)
            subresult = cls.get_page(response.json()['robots'], page, per_page)

            result = []
            for robot in subresult:
                robot_obj = api_model.Robot.from_json(robot)
                if full:
                    robot_obj.get_runs()
                cls.last_loaded_robots[robot_obj.robot_id] = robot_obj
                result.append(robot_obj)

            return result
        except Exception as e:
            print(f"[ERR] Can't get robots list: {e}")
            return []
    @classmethod
    def get_robot(cls, robot_id, full=True):
        try:
            result = api_model.Robot.from_id(robot_id)
            if full:
                result.get_runs()

            return result
        except Exception as e:
            print(f"[ERR] Can't get robot {robot_id}: {e}")
            return {}

    @classmethod
    def get_services_list(cls, full=True, page=1, per_page=10):
        try:
            url = f'{cls.api_endpoint}/services'
            response = requests.get(url)
            subresult = cls.get_page(response.json()['services'], page, per_page)
            print(f"[DBG][get_services_list] subresult = '{subresult}'")

            result = []
            for service in subresult:
                service_obj = api_model.Service.from_json(service)

                print(f"[DBG][get_services_list] service_obj = '{service_obj}'")

                # Пока прикомментил, но вероятно нам это не понадобится в будущем
                #if full:
                #    service_obj.get_business_processes()
                cls.last_loaded_services[service_obj.service_id] = service_obj
                result.append(service_obj)

            return result
        except Exception as e:
            print(f"[ERR] Can't get services list: {e}")
            return []

    @classmethod
    def get_service(cls, service_id, full=True):
        try:
            result = api_model.Service.from_id(service_id)
            if full:
                result.get_business_processes()

            return result
        except Exception as e:
            print(f"[ERR] Can't get service {service_id}: {e}")
            return {}

    @classmethod
    def get_business_processes_list(cls, full=True, page=1, per_page=10):
        try:
            url = f'{cls.api_endpoint}/processes'
            response = requests.get(url)
            subresult = cls.get_page(response.json()['processes'], page, per_page)

            print(f"[DBG][get_business_processes_list] subresult: {subresult}")

            result = []
            for business_process in subresult:
                business_process_obj = api_model.BusinessProcess.from_json(business_process)

                cls.last_loaded_business_processes[business_process_obj.process_id] = business_process_obj
                result.append(business_process_obj)

            return result
        except Exception as e:
            print(f"[ERR] Can't get business processes list: {e}")
            return []

    @classmethod
    def get_business_process(cls, business_process_id, full=True):
        try:
            result = api_model.BusinessProcess.from_id(business_process_id)
            if full:
                result.get_transactions()

            return result
        except Exception as e:
            print(f"[ERR] Can't get business process {business_process_id}: {e}")
            return {}

    @classmethod
    def get_transaction_list(cls, full=True, page=1, per_page=10):
        try:
            url = f'{cls.api_endpoint}/transactions'

            response = requests.get(url)

            print(f"[DBG][get_transaction_list] response: {response.json()}")

            subresult = cls.get_page(response.json()['transactions'], page, per_page)

            result = []
            for transaction in subresult:
                transaction_obj = api_model.Transaction.from_json(transaction)

                # Поживем пока без этого
                # if full:
                #    transaction_obj.get_steps()
                #    transaction_obj.get_runs()
                # transaction_obj.process = cls.last_loaded_business_processes[transaction_obj.process_id].name
                # cls.last_loaded_transactions[transaction_obj.transaction_id] = transaction_obj
                result.append(transaction_obj)

            return result
        except Exception as e:
            print(f"[ERR][get_transaction_list] Can't get transactions list: {e}")
            return []

    @classmethod
    def get_transaction(cls, transaction_id, full=True):
        try:
            result = api_model.Transaction.from_id(transaction_id)
            if full:
                result.get_runs()
                result.get_steps()

            return result
        except Exception as e:
            print(f"[ERR] Can't get transaction {transaction_id}: {e}")
            return {}

    @classmethod
    def get_transaction_steps(cls, transaction_id, full=True, page=1, per_page=10):
        try:
            transaction = cls.get_transaction(transaction_id, full=False)
            result = cls.get_page(transaction.get_steps(), page, per_page)

            if full:
                for step in result:
                    step.get_runs()

            return result
        except Exception as e:
            print(f"[ERR] Can't get steps for transaction {transaction_id}: {e}")
            return []

    @classmethod
    def get_step(cls, step_id, full=True):
        try:
            result = api_model.Step.from_id(step_id)
            if full:
                result.get_runs()

            return result
        except Exception as e:
            print(f"[ERR] Can't get step {step_id}: {e}")
            return {}

    @classmethod
    def get_transaction_runs(cls, transaction_id=None, robot_id=None, page=1, per_page=10):
        try:
            if transaction_id:
                transaction = cls.get_transaction(transaction_id, full=False)
                result = cls.get_page(transaction.get_runs(), page, per_page)
            elif robot_id:
                robot = cls.get_robot(robot_id, full=False)
                result = robot.get_runs()
            else:
                result = []

            return result
        except Exception as e:
            print(f"[ERR] Can't get runs for transaction {transaction_id}: {e}")
            return []

    @classmethod
    def get_step_runs(cls, step_id, run_result=None, page=1, per_page=10):
        try:
            step = cls.get_step(step_id, full=False)
            result = cls.get_page(step.get_runs(run_result), page, per_page)

            return result
        except Exception as e:
            print(f"[ERR] Can't get runs for step {step_id}: {e}")
            return []

    @classmethod
    def get_run_steps(cls, run_id, page=1, per_page=10):
        try:
            run = api_model.TransactionRun.from_id(run_id)
            result = cls.get_page(run.get_steps(), page, per_page)

            return result
        except Exception as e:
            print(f"[ERR] Can't get steps for run {run_id}: {e}")
            return []

    @classmethod
    def download_file(cls, fileclass, id):
        try:
            virtual_file = io.BytesIO()
            url = f'{cls.api_endpoint}/{fileclass}/{id}'
            response = requests.get(url)
            virtual_file.write(response.content)
            virtual_file.seek(0)

            mime_type = response.headers['Content-Type']
            return virtual_file, mime_type
        except Exception as e:
            print(f"[ERR] Can't download file {fileclass}/{id}: {e}")
            return None, None

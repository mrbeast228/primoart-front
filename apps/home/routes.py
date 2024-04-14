    # -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from apps.home import blueprint
from flask import render_template, request
from flask_login import login_required, current_user
from jinja2 import TemplateNotFound

from apps.home.api_connector import APIConnector
from apps.home.api_model import *

from datetime import datetime, timedelta

class RouterHelper:
    @staticmethod
    def get_segment(request):
        try:
            segment = request.path.split('/')[-1]
            return segment if segment else 'index'
        except:
            return None

    @staticmethod
    def create_context(template):
        ctx = {'sla_target': APIBase.sla_target}
        id_type = 'empty'

        page_number = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)

        if template == 'mvp-main-dashboard.html':
            current_process_id = request.args.get('project_id', None, type=str)

            ctx['services'] = APIConnector.get_services_list(page=page_number, per_page=per_page, process_id=current_process_id)
            print(f"[DBG][create_context] ctx['services'] = '{ctx['services']}'")
            ctx['projects'] = APIConnector.get_business_processes_list(page=page_number, per_page=per_page)
            print(f"[DBG][create_context] ctx['projects'] = '{ctx['projects']}'")
            ctx['robots'] = APIConnector.get_robots_list(page=page_number, per_page=per_page)
            print(f"[DBG][create_context] ctx['robots'] = '{ctx['robots']}'")

            if current_process_id:
                ctx['current_process'] = APIConnector.get_business_process(current_process_id)
                print(f"[DBG][create_context] ctx['current_process'] = '{ctx['current_process']}'")
            else:
                ctx['current_process'] = None
                # add global SLA for all processes
                ctx['global_sla'] = GlobalSLA.from_api()

        elif template == 'mvp-objects-projects.html':
            ctx['projects'] = APIConnector.get_business_processes_list(page=page_number, per_page=per_page)
            print(f"[DBG][create_context] ctx['projects'] = '{ctx['projects']}'")

        elif template == 'mvp-objects-services.html':
            ctx['projects'] = APIConnector.get_business_processes_list(page=page_number, per_page=per_page)
            print(f"[DBG][create_context] ctx['projects'] = '{ctx['projects']}'")
            ctx['services'] = APIConnector.get_services_list(page=page_number, per_page=per_page)
            print(f"[DBG][create_context] ctx['services'] = '{ctx['services']}'")

        elif template == 'mvp-objects-robots.html':
            ctx['robots'] = APIConnector.get_robots_list(page=page_number, per_page=per_page)
            print(f"[DBG][create_context] ctx['robots'] = '{ctx['robots']}'")

        elif template == 'mvp-objects-transactions.html':
            ctx['services'] = APIConnector.get_services_list(page=page_number, per_page=per_page)
            print(f"[DBG][create_context] ctx['services'] = '{ctx['services']}'")

            ctx['transactions'] = APIConnector.get_transaction_list(page=page_number, per_page=per_page)
            print(f"[DBG][create_context] ctx['transactions'] = '{ctx['transactions']}'")

        elif template == 'mvp-services.html':
            ctx['services'] = APIConnector.get_services_list(page=page_number, per_page=per_page)
            print(f"[DBG][create_context] ctx['services'] = '{ctx['services']}'")
            ctx['projects'] = APIConnector.get_business_processes_list(page=page_number, per_page=per_page)
            print(f"[DBG][create_context] ctx['projects'] = '{ctx['projects']}'")
            ctx['robots'] = APIConnector.get_robots_list(page=page_number, per_page=per_page)
            print(f"[DBG][create_context] ctx['robots'] = '{ctx['robots']}'")

            # TODO: реализовать возможность передачи ID сервиса, робота или проекта
            ctx['transactions'] = APIConnector.get_transaction_list(page=page_number, per_page=per_page)
            print(f"[DBG][create_context] ctx['transactions'] = '{ctx['transactions']}'")

        elif template == 'mvp-transaction.html':
            transaction_id = request.args.get('transaction_id', None, type=str)

            ctx['transaction'] = APIConnector.get_transaction(transaction_id=transaction_id, full=False)
            print(f"[DBG][create_context] ctx['transaction'] = '{ctx['transaction']}'")
            ctx['runs'] = APIConnector.get_transaction_runs(transaction_id=transaction_id, page=page_number, per_page=per_page)
            print(f"[DBG][create_context] ctx['runs'] = '{ctx['runs']}'")


        elif template == 'robot_list.html':
            ctx['robots'] = APIConnector.get_robots_list(page=page_number, per_page=per_page)



        elif template == 'step_list.html':
            transaction_id = request.args.get('transaction_id', None, type=str)
            ctx['steps'] = APIConnector.get_transaction_steps(transaction_id, page=page_number, per_page=per_page) if transaction_id else []

        elif template == 'transaction_runs.html':
            transaction_id = request.args.get('transaction_id', None, type=str)
            robot_id = request.args.get('robot_id', None, type=str)
            if transaction_id:
                ctx['runs'] = APIConnector.get_transaction_runs(transaction_id=transaction_id, page=page_number, per_page=per_page)
            elif robot_id:
                ctx['runs'] = APIConnector.get_transaction_runs(robot_id=robot_id, page=page_number, per_page=per_page)
            else:
                ctx['runs'] = []

        elif template == 'step_runs.html':
            step_id = request.args.get('step_id', None, type=str)
            run_id = request.args.get('run_id', None, type=str)
            if step_id:
                ctx['runs'] = APIConnector.get_step_runs(step_id, page=page_number, per_page=per_page)
                id_type = 'step'
            elif run_id:
                ctx['runs'] = APIConnector.get_run_steps(run_id, page=page_number, per_page=per_page)
                id_type = 'run'
            else:
                ctx['runs'] = []
                id_type = 'run'

        return ctx, id_type

    @staticmethod
    def is_number(s):
        try:
            float(s)
            return True
        except ValueError:
            return False

    # special function to convert statuses from database to badge of our current CSS
    @staticmethod
    def badger(status):
        if status == "OK" or RouterHelper.is_number(status) and status > 90: # combo for strings and percentages
            return "success"
        if status == "WARNING" or RouterHelper.is_number(status) and status > 70:
            return "warning"
        if status == "FAIL" or RouterHelper.is_number(status) and status <= 70:
            return "danger"
        return "neutral"


@blueprint.route('/index')
@login_required
def index():
    index_page = 'mvp-main-dashboard.html'
    return route_template(index_page)
    #return render_template('home/index.html',
    #                       segment='index',
    #                       user_id=current_user.id)

@blueprint.route('/<template>')
@login_required
def route_template(template):

    try:

        if not template.endswith('.html'):
            template += '.html'

        # Detect the current page
        # В переменную segment приезжает название страницы (соответствует шаблону в templates/home)
        segment = RouterHelper.get_segment(request)
        action = request.form.get('action')

        print(f"[DBG][route_template] request: {request}")
        print(f"[DBG][route_template] action: {action}")
        print(f"[DBG][route_template] template: {template}")
        print(f"[DBG][route_template] segment: {segment}")

        # Q: Непонятно назначение этой штуки
        fmts = {
            'fmt_datetime': "%Y-%m-%d %H:%M:%S.%f",
            'fmt_date_output': "%Y-%m-%d %H:%M:%S"
        }
        ctx, id_type = RouterHelper.create_context(template)

        # Serve the file (if exists) from app/templates/home/FILE.html
        return render_template("home/" + template, segment=segment, context=ctx, str=str,
                                     badger=RouterHelper.badger, fmts=fmts, id_type=id_type)

    except TemplateNotFound:
        return render_template('home/page-404.html'), 404

    except Exception as e:
        print(f"[ERR] route_template: {e}")
        return render_template('home/page-500.html'), 500


@blueprint.route('/data/projects/get')
@login_required
def r_data_projects_get():
    return [{"a": 1}, {"b": 2}, {"c": 3}]

@blueprint.route('/data/projects/add', methods=["POST"])
@login_required
def r_data_projects_add():
    params = request.json
    print(f"[DBG][r_data_projects_add] params: {params}")

    name = params["name"]
    description = params["description"]
    target_sla = params["target_sla"]
    owner = params["owner"]

    result = BusinessProcess.add(name, description, owner)

    print(f"[DBG][r_data_projects_add] result: {result}")

    return result

@blueprint.route('/data/projects/edit', methods=["POST"])
@login_required
def r_data_projects_edit():

    params = request.json
    print(f"[DBG][r_data_projects_edit] params: {params}")

    process_id = params["project_id"]
    name = params["name"]
    description = params["description"]
    target_sla = params["target_sla"]
    owner = params["owner"]

    result = BusinessProcess.edit(process_id, name, description, owner)

    print(f"[DBG][r_data_projects_edit] result: {result}")

    return result

@blueprint.route('/data/projects/delete', methods=["POST"])
@login_required
def r_data_projects_delete():

    params = request.json
    print(f"[DBG][r_data_projects_delete] params: {params}")

    results = []

    for project in params:
        project_id = project["project_id"]
        result = BusinessProcess.delete(project_id)

        results.append(result)

    return results

@blueprint.route('/data/services/add', methods=["POST"])
@login_required
def r_data_services_add():
    params = request.json
    print(f"[DBG][r_data_services_add] params: {params}")

    project_id = params["project"]
    name = params["name"]
    description = params["description"]
    target_sla = params["target_sla"]
    owner = params["owner"]

    result = Service.add(project_id, name, description, owner)

    print(f"[DBG][r_data_services_add] result: {result}")

    return result

@blueprint.route('/data/services/edit', methods=["POST"])
@login_required
def r_data_services_edit():

    params = request.json
    print(f"[DBG][r_data_services_edit] params: {params}")

    service_id = params["service_id"]
    project_id = params["project"]
    name = params["name"]
    description = params["description"]
    target_sla = params["target_sla"]
    owner = params["owner"]

    result = Service.edit(service_id, project_id, name, description, owner)

    print(f"[DBG][r_data_services_edit] result: {result}")

    return result

@blueprint.route('/data/services/delete', methods=["POST"])
@login_required
def r_data_services_delete():

    params = request.json
    print(f"[DBG][r_data_services_delete] params: {params}")

    results = []

    for service in params:
        service_id = service["service_id"]
        result = Service.delete(service_id)

        results.append(result)

    return results

@blueprint.route('/data/services')
@login_required
def r_data_services():
    return Service.list_all()

@blueprint.route('/data/robots')
@login_required
def r_data_robots():
    return [{"a": 1}, {"b": 2}, {"c": 3}]

@blueprint.route('/data/transactions')
@login_required
def r_data_transactions():
    return Transaction.list_all()

@blueprint.route('/data/steps')
@login_required
def r_data_steps():
    return [{"a": 1}, {"b": 2}, {"c": 3}]

@blueprint.route('/data/runs')
@login_required
def r_data_runs():
    return TransactionRun.list_all()

@blueprint.route('/charts/heatmap')
@login_required
def r_charts_heatmap():
    filter_json = {}
    for idtype in 'process', 'service', 'transaction':
        if f'{idtype}_id' in request.args:
            filter_json[f'{idtype}id'] = request.args[f'{idtype}_id']
            break
    return Charts.get_heatmap(filter_json)

@blueprint.route('/charts/runs')
@login_required
def r_charts_runs():
    service_id = request.args["service_id"]
    start_time = request.args["start_time"]
    end_time = request.args["end_time"]

    runs = Charts.get_transaction_runs(service_id=service_id, start_time=start_time, end_time=end_time)

    res = {"OK": [], "Failed": []}

    for run in runs:
        response_time = (datetime.strptime(run["runend"], "%Y-%m-%d %H:%M:%S.%f") - datetime.strptime(run["runstart"],"%Y-%m-%d %H:%M:%S.%f")).microseconds
        response_time = round(response_time/1000, 2)
        cur = {
            "x": run["runstart"],
            "y": response_time
        }
        res["OK" if run["runresult"] == "OK" else "Failed"].append(cur)

    return res

@blueprint.route('/charts/timevserr')
@login_required
def r_charts_timevserr():
    start_time = request.args["start_time"]
    end_time = request.args["end_time"]
    process_id = request.args.get("process_id", None)
    service_id = request.args.get("service_id", None) # TODO

    res = []

    if not process_id:
        services = APIConnector.get_services_list()['services']
    else:
        services = APIConnector.get_services_list(process_id=process_id)['services']

    for service in services:
        runs = Charts.get_transaction_runs(service_id=str(service.service_id), start_time=start_time, end_time=end_time)
        err_percentage = round((len(list(filter(lambda x: x["runresult"] == "FAIL", runs)))) / (len(runs)),4)*100
        all_time = sum([(datetime.strptime(run["runend"], "%Y-%m-%d %H:%M:%S.%f") - datetime.strptime(run["runstart"],"%Y-%m-%d %H:%M:%S.%f")).microseconds/1000 for run in runs])
        average_time = round(all_time / len(runs), 2)
        res.append({"service_name": service.name, "err_percentage": err_percentage, "average_time": average_time})

    res.sort(key=lambda x: x["err_percentage"])

    return res

def get_daily_runs(start_time, end_time, process_id=None):
    start_date = datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S.%f").date()
    end_date = datetime.strptime(end_time, "%Y-%m-%d %H:%M:%S.%f").date()
    period_len = (end_date - start_date).days + 1

    result = [{"date": start_date + timedelta(days=i), "runs": []} for i in range(period_len)]

    services_id = [str(service.service_id) for service in APIConnector.get_services_list(process_id=process_id)["services"]]

    all_runs = Charts.get_transaction_runs(service_id=services_id, start_time=start_time, end_time=end_time)

    for run in all_runs:
        run_date = datetime.strptime(run["runstart"], "%Y-%m-%d %H:%M:%S.%f").date()
        result[(run_date - start_date).days]["runs"].append(run)

    return result

@blueprint.route('/charts/perfomance')
@login_required
def r_charts_perfomance():
    start_time = request.args["start_time"]
    end_time = request.args["end_time"]
    process_id = request.args.get("process_id", None)

    daily_runs = get_daily_runs(start_time=start_time, end_time=end_time, process_id=process_id)

    res = []

    for day in daily_runs:
        date = day["date"]
        num_all_runs = len(day["runs"])
        num_err_runs = len(list(filter(lambda run: run["runresult"] == "FAIL", day["runs"])))
        res.append({"date": date.strftime("%Y-%m-%d"), "all_num": num_all_runs, "err_num": num_err_runs})

    return res

@blueprint.route('/charts/step_run')
@login_required
def r_charts_step_run():
    trx_run_id = request.args["transaction_run_id"]
    trx_run = TransactionRun.from_id(trx_run_id)

    res = []
    for step_run in trx_run.get_steps():
        res.append({
            "step_name": step_run.step_name,
            "time": (step_run.run_end - step_run.run_start).total_seconds(),
            "status": step_run.run_result,
        })
    res.sort(key=lambda x: x["time"])

    return res

@blueprint.route('/charts/transaction_robots')
# @login_required
def r_charts_transaction_robots():
    trx_id = request.args["transaction_id"]
    trx = Transaction.from_id(trx_id, robots=True)

    res = []

    for robot in trx.robots:
        res.append({
            "name": robot.name,
            "stats": robot.stats,
        })

    return res

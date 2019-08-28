import json
from threading import Thread
from queue import Queue

from migration.json_decoder import get_workload, get_migration
from migration.workload import Workload

from api.listener import Listener

from persistence.workload import WorkloadPickler
from persistence.migration import MigrationPickler

from flask import Flask
from flask import request
from flask import Response
app = Flask(__name__)
q = Queue()


@app.route('/')
def hello():
    return "Hello World!"


@app.route('/workloads/add', methods=['POST'])
def add_workload():
    try:
        workload_data = str(request.data, 'utf-8')
        workload = get_workload(workload_data)
        workload_pickler = WorkloadPickler()
        workload_pickler.create(workload)
    except Exception as e:
        response_json = {"success": False, "error": str(e)}
        return Response(json.dumps(response_json), status=500, mimetype='application/json')

    response_json = {"success": True, "error": None}
    return Response(json.dumps(response_json), status=200, mimetype='application/json')


@app.route('/workloads/delete', methods=['POST'])
def delete_workload():
    try:
        workload_data = str(request.data, 'utf-8')
        workload = get_workload(workload_data)
        workload_pickler = WorkloadPickler()
        workload_pickler.delete(workload)
    except Exception as e:
        response_json = {"success": False, "error": str(e)}
        return Response(json.dumps(response_json), status=500, mimetype='application/json')

    response_json = {"success": True, "error": None}
    return Response(json.dumps(response_json), status=200, mimetype='application/json')


@app.route('/workloads/update', methods=['POST'])
def update_workload():
    try:
        workloads_data = json.loads(request.data)

        old_workload = get_workload(json.dumps(workloads_data['old']))
        new_workload = get_workload(json.dumps(workloads_data['new']))
        workload_pickler = WorkloadPickler()
        workload_pickler.update(old_workload, new_workload)
    except Exception as e:
        response_json = {"success": False, "error": str(e)}
        return Response(json.dumps(response_json), status=500, mimetype='application/json')

    response_json = {"success": True, "error": None}
    return Response(json.dumps(response_json), status=200, mimetype='application/json')


@app.route('/migrations/run', methods=['POST'])
def run_migration():
    try:
        migration_data = str(request.data, 'utf-8')

        migration = get_migration(migration_data)
        migration_pickler = MigrationPickler()
        migrations = migration_pickler.read(migration)

        if len(migrations) == 0:
            raise Exception("There are no such migrations at persistence layer")

        if len(migrations) > 1:
            raise Exception("There are more than one such migration at persistence layer")

        migration_to_run = migrations[0]
        q.put(migration_to_run)
    except Exception as e:
        response_json = {"success": False, "error": str(e)}
        return Response(json.dumps(response_json), status=500, mimetype='application/json')

    response_json = {"success": True, "error": None}
    return Response(json.dumps(response_json), status=200, mimetype='application/json')


@app.route('/migrations/status', methods=['POST'])
def get_migration_status():
    try:
        migration_data = str(request.data, 'utf-8')
        migration = get_migration(migration_data)
        migration_pickler = MigrationPickler()
        migrations = migration_pickler.read(migration)

        if len(migrations) == 0:
            raise Exception("There are no such migrations at persistence layer")

        if len(migrations) > 1:
            raise Exception("There are more than one such migration at persistence layer")

        response_json = {"status": migrations[0].migration_state.name, "error": None}
        return Response(json.dumps(response_json), status=200, mimetype='application/json')
    except Exception as e:
        response_json = {"success": False, "error": str(e)}
        return Response(json.dumps(response_json), status=500, mimetype='application/json')


if __name__ == '__main__':
    queue_listener = Listener()
    Thread(target=app.run).start()
    Thread(target=queue_listener.run, args=(q,)).start()


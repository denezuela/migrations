import json

from migration.json_decoder import get_workload
from migration.workload import Workload

from persistence.workload import WorkloadPickler
from flask import Flask
from flask import request
from flask import Response
app = Flask(__name__)


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


if __name__ == '__main__':
    app.run()
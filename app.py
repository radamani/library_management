import datetime
import json
import os
import requests
import re
import sys
from threading import Thread
import pandas as pd
import traceback
from flask import Flask
from flask_cors import CORS
from flask import request
from flask import Response
sys.path.append(os.getcwd() + '\\controller\\')
sys.path.append(os.getcwd() + '\\worker\\')
import library_maintenance_controller as lmc


app = Flask(__name__)
CORS(app)


@app.route('/<report_name>', methods=['GET', 'POST'])
def router(report_name):
    try:
        print(os.getcwd())
        worker_name = re.findall('/(\w+)\?', str(request))[0]
        arg = (request.args.to_dict())
        params = {"worker_name": worker_name}
        arg.update(params)
        print(arg)
        res = lmc.basic(arg)
        return res

    except Exception as e:
        print(traceback.print_exec())
        data = {
            'Msg': 'Something Went Wrong. Please Try Again',
            'Error': str(e)
        }
        js = json.dumps(data)
        resp = Response(js, status=500, mimetype='application/json')
        return resp


if __name__ == '__main__':
    app.run()
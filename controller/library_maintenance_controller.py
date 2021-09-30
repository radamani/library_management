import json, sys, os
from flask import Response
from threading import Thread
sys.path.append(os.getcwd() + '\\worker\\')
import worker.library_worker as worker


def basic(args):
    try:
        #thread = Thread(target=worker.library_call, kwargs=args)
        #thread.start()
        resp = worker.library_call(**args)
        return resp
    except Exception as e:
        print(str(e))
        data = {
            "Error Msg": "Something went wrong in starting worker. Please try Again"
        }
        js = json.dumps(data)
        resp = Response(js, status=500, mimetype='application/json')
        return resp
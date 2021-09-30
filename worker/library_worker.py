import json, sys, os, binascii, traceback
from flask import request
from flask import Response
import pandas as pd
sys.path.append(os.getcwd() + '\\manage\\')
import manage.library_manager as manager


function_map = {
    "library_book_update": manager.library_book_update,
    "book_update": manager.book_update,
    "library_activities": manager.library_activities,
    "library_activity_user": manager.library_activity_user,
    "library_activity_overall": manager.library_activity_overall
}

update_calls = ['library_book_update', 'book_update', 'library_activities']

fetch_calls = ['library_activity_user', 'library_activity_overall']


def library_call(**arg):
    try:

        response_data = (function_map[arg.get('worker_name')])(**arg)
        return response_data

    except Exception as e:
        print('Function call exception' + str(e))
        print('Function call exception' + arg.get('worker_name'))
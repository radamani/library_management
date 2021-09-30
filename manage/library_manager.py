import sqlite3
import traceback
import json
import pandas as pd
from flask import Response
#import pymysql
#con = pymysql.connect()
con = sqlite3.connect('C:\sqlite3\library_schema.db', check_same_thread=False)
print(con)
cursor = con.cursor()


def library_activity_overall(**arg):
    try:
        print('inside library activity user')
        library_id = arg.get('library_id')
        library_checkout_query = """select l.name, la.activity_type, b.title, b.author_name, checked_out_at, checked_in_at
        from library_activities la left join library_books lb using(library_book_id)  left join books b using(book_id) 
        left join libraries l using(library_id) where library_id = 2 and 
        activity_type = 'checkout';""".format(library_id)
        cursor.execute(library_checkout_query)
        result = cursor.fetchall()
        column = ['library_name', 'activity_type', 'title', 'author_name', 'checked_out_at', 'checked_in_at']
        library_checkout_data = pd.DataFrame(result, columns=column)
        library_checkout_data = library_checkout_data.to_dict(orient='records')
        library_checkout_data = json.dumps(library_checkout_data)
        print(library_checkout_data)
        return library_checkout_data

    except Exception as e:
        print(str(traceback.print_exc()))


def library_activity_user(**arg):
    try:
        print('inside library activity user')
        user_name = arg.get('name')
        user_checkout_query = """select u.name, la.activity_type, b.title, b.author_name, checked_out_at, checked_in_at
        from users u left join library_activities la using(user_id) left join library_books lb using(library_book_id) 
        left join books b using(book_id) where lower(u.name) = '{0}' and activity_type = 'checkout';""".format(user_name.lower())
        cursor.execute(user_checkout_query)
        result = cursor.fetchall()
        column = ['user_name', 'activity_type', 'title', 'author_name', 'checked_out_at', 'checked_in_at']
        user_checkout_data = pd.DataFrame(result, columns=column)
        user_checkout_data = user_checkout_data.to_dict(orient='records')
        user_checkout_data = json.dumps(user_checkout_data)
        print(user_checkout_data)
        return user_checkout_data

    except Exception as e:
        print(str(traceback.print_exc()))


def library_activities(**arg):
    try:
        activity_type = arg.get('activity_type')
        user_id = arg.get('user_id')
        library_book_id = arg.get('library_book_id')
        checked_out_at = arg.get('checked_out_at')
        checked_in_at = arg.get('checked_in_at')
        print(activity_type, user_id, library_book_id, checked_out_at, checked_in_at)

        check_existing = """select * from library_activities where user_id = '{0}'
        and library_book_id = '{1}' and (checked_in_at is null or checked_in_at = '' or checked_out_at is null or 
        checked_out_at = '') 
        order by library_activity_id desc limit 1;""".format(user_id, library_book_id)
        cursor.execute(check_existing)
        result = cursor.fetchall()

        if len(result) == 0:

            insert_query = """insert into library_activities (activity_type, user_id, library_book_id, checked_out_at, 
            checked_in_at) values('{0}', '{1}', '{2}', '{3}', '{4}')""".format(activity_type, user_id, library_book_id,
                                                                               checked_out_at, checked_in_at)
            print(insert_query)
            cursor.execute(insert_query)
            cursor.execute('commit')

        else:
            update_query = """update library_activities set checked_in_at = '{0}', activity_type = '{3}'
            where user_id = '{1}' and library_book_id = '{2}'""".format(checked_in_at, user_id, library_book_id, activity_type)
            cursor.execute(update_query)
            cursor.execute('commit')

        last_activity_query = """select library_activity_id from library_activities where user_id = '{0}'
        and library_book_id = '{1}'  
        order by library_activity_id desc limit 1;""".format(user_id, library_book_id)
        cursor.execute(last_activity_query)
        last_activity = cursor.fetchall()

        update_last_activity = """update library_books set last_library_activity_id = '{0}' 
        where library_book_id = '{1}'""".format(last_activity[0][0], library_book_id)
        cursor.execute(update_last_activity)
        cursor.execute('commit')

        data = {
            'Msg': 'Data Saved Successfully'
        }
        js = json.dumps(data)
        resp = Response(js, status=200, mimetype='application/json')
        return resp

    except Exception as e:
        print(str(traceback.print_exc()))


def book_update(**arg):
    try:
        title = arg.get('title')
        author_name = arg.get('author_name')
        isbn_num = arg.get('isbn_num')
        genre = arg.get('genre')
        description = arg.get('description')
        print(title, author_name, isbn_num, genre, description)

        insert_query = """insert into books (title, author_name, genre, isbn_num, description) 
        values('{0}','{1}','{2}','{3}', '{4}')""".format(title, author_name, genre, isbn_num, description)
        print(insert_query)
        cursor.execute(insert_query)
        cursor.execute('commit')

        data = {
            'Msg': 'Data Saved Successfully'
        }
        js = json.dumps(data)
        resp = Response(js, status=200, mimetype='application/json')
        return resp

    except Exception as e:
        print(str(traceback.print_exc()))


def library_book_update(**arg):
    try:
        print('inside library update function')
        book_id = arg.get('book_id')
        library_id = arg.get('library_id')

        insert_query = """insert into library_books (book_id, library_id) 
        values('{0}', '{1}')""".format(book_id, library_id)

        print(insert_query)
        cursor.execute(insert_query)
        cursor.execute('commit')
        data = {
            'Msg': 'Data Saved Successfully'
        }
        js = json.dumps(data)
        resp = Response(js, status=200, mimetype='application/json')
        return resp

    except Exception as e:
        print(str(traceback.print_exc()))
from django.db import connection
import datetime
import uuid

def execute_query(query):
    with connection.cursor() as cursor:
        cursor.execute(query)
        columns = [col[0] for col in cursor.description]
        # results = cursor.fetchall()
        results = [
            dict(zip(columns, (str(val) if isinstance(val, uuid.UUID) 
                                else val.strftime("%d %B %Y - %H:%M") if isinstance(val, datetime.datetime) 
                                else val.strftime("%Y-%m-%d") if isinstance(val, datetime.date) 
                                else val.strftime("%H:%M") if isinstance(val, datetime.time) 
                                else val for val in row)))
            for row in cursor.fetchall()
        ]
    return results

def execute_query2(query):
    try:
        with connection.cursor() as cursor:
            cursor.execute(query)
            columns = [col[0] for col in cursor.description]
            results = [
                dict(zip(columns, (str(val) if isinstance(val, uuid.UUID) 
                                    else val.strftime("%d %B %Y - %H:%M") if isinstance(val, datetime.datetime) 
                                    else val.strftime("%Y-%m-%d") if isinstance(val, datetime.date) 
                                    else val.strftime("%H:%M") if isinstance(val, datetime.time) 
                                    else val for val in row)))
                for row in cursor.fetchall()
            ]
        return results
    except Exception as e:
        # Handle the exception or log the error message
        print(f"Error executing query: {query}\n{e}")
        return []


def commit_query(query):
    with connection.cursor() as cursor:
        cursor.execute(query)
        connection.commit()
from django.db import connections
from utils.DBUtils import execute_query
from django.http import HttpResponseRedirect

def login_required(func):
    def wrapper(*args, **kwargs):
        req = args[0]
        email = req.session["email"]
        password = req.session["password"]

        if email is None:
            return HttpResponseRedirect("/")

        with connections["sirest"].cursor() as cursor:
            query = f"""
            SELECT * FROM USER_ACC
            WHERE email='{email}' AND password='{password}'
            """
            cursor.execute(query)
            result = cursor.fetchall()

            if not result:
                return HttpResponseRedirect("/")

        return func(*args, **kwargs)

    return wrapper
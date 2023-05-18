from django.shortcuts import redirect
from utils.DBUtils import execute_query
from django.http import HttpResponseRedirect

def login_required(function):
    def wrapper(request, *args, **kwargs):
        
        if not request.session.get('code_success'):
            return HttpResponseRedirect("/")
        
        username = request.session["username"]
        password = request.session["password"]

        if username is None:
            return HttpResponseRedirect("/")

        query = f"""
        SELECT * FROM user_system
        WHERE username='{username}' AND password='{password}'
        """
        result = execute_query(query)

        if not result:
            return HttpResponseRedirect("/")

        return function(request, *args, **kwargs)

    return wrapper
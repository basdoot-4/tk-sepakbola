from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import redirect, render
from utils.DBUtils import execute_query
from utils.decorator import login_required

# Create your views here.
def index(request):
    return render(request, 'index.html')

def register(request):
    return render(request, 'register.html')

def register_manajer(request):
    return render(request, 'register-manajer.html')

def register_panitia(request):
    return render(request, 'register-panitia.html')

def register_penonton(request):
    return render(request, 'register-penonton.html')

def login(request):
    return render(request, 'login.html')

def login_post(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        
        query = f"""
        SELECT * FROM user_system
        WHERE username='{username}' AND password='{password}'
        """
        result = execute_query(query)
        print(result)
        
        if result:
            role=""
            
            # role manajer
            query = f"""
            SELECT * FROM manajer
            WHERE username='{username}'
            """
            result = execute_query(query)

            if result:
                role = "manajer"
                
            # role manajer
            query = f"""
            SELECT * FROM penonton
            WHERE username='{username}'
            """
            result = execute_query(query)

            if result:
                role = "penonton"
                
            # role manajer
            query = f"""
            SELECT * FROM panitia
            WHERE username='{username}'
            """
            result = execute_query(query)

            if result:
                role = "panitia"
            
            request.session["username"] = username
            request.session["password"] = password
            request.session["role"] = role
            print(role, username, password)
            
            return redirect('/dashboard')
    
    return redirect('/login')

@login_required
def dashboard(request):
    role = request.session["role"]
    if role == "manajer":
        return render(request, 'dashboard-manajer.html')
    elif role == "panitia":
        return render(request, 'dashboard-panitia.html')
    else:
        return render(request, 'dashboard-penonton.html')

@login_required
def logout(request):
    del request.session["username"]
    del request.session["password"]
    del request.session["role"]
    
    return redirect('/')
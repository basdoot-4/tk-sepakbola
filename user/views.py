from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import redirect, render
from django.contrib import messages
from utils.DBUtils import execute_query, execute_query2
from utils.decorator import login_required
import uuid
import string
import random

# Create your views here.
def index(request):
    return render(request, 'index.html')

def register(request):
    return render(request, 'register.html')

def register_manajer(request):
    if request.method == "GET":
        return render(request, "register-manajer.html")

    id_manajer = generate_id()
    username = generate_username(request.POST['firstName'],request.POST['lastName'])  # Generate the username as per your requirements
    password = generate_password()  # Generate the password as per your requirements

    print(f"Username: {username}")
    print(f"Password: {password}")

    try:
        # Insert into USER_SYSTEM table
        insert_user = f"INSERT INTO USER_SYSTEM (username, password) " \
                      f"VALUES ('{username}', '{password}')"
        execute_query2(insert_user)

        # Insert into NON_PEMAIN table
        insert_non_pemain = f"INSERT INTO NON_PEMAIN (id, nama_depan, nama_belakang, nomor_hp, email, alamat) " \
                            f"VALUES ('{id_manajer}', '{request.POST['firstName']}', '{request.POST['lastName']}', " \
                            f"'{request.POST['phoneNumber']}', '{request.POST['email']}', '{request.POST['address']}')"
        execute_query2(insert_non_pemain)

        # Insert into PANITIA table
        insert_manajer = f"INSERT INTO MANAJER (id_panitia, username) " \
                         f"VALUES ('{id_manajer}', '{username}')"
        execute_query2(insert_manajer)

    except Exception as e:
        error_msg = generate_error_message(e)
        messages.error(request, generate_error_message(e))
        
        return render(request, "register-manajer.html")
    
    return render(request, 'register-manajer.html')

# Function untuk register panitia
def register_panitia(request):
    if request.method == "GET":
        return render(request, "register-panitia.html")

    id_panitia = generate_id()
    jabatan = request.POST['jabatan']
    username = generate_username(request.POST['firstName'],request.POST['lastName'])  # Generate the username as per your requirements
    password = generate_password()  # Generate the password as per your requirements

    print(f"Username: {username}")
    print(f"Password: {password}")

    try:
        # Insert into USER_SYSTEM table
        insert_user = f"INSERT INTO USER_SYSTEM (username, password) " \
                      f"VALUES ('{username}', '{password}')"
        execute_query2(insert_user)

        # Insert into NON_PEMAIN table
        insert_non_pemain = f"INSERT INTO NON_PEMAIN (id, nama_depan, nama_belakang, nomor_hp, email, alamat) " \
                            f"VALUES ('{id_panitia}', '{request.POST['firstName']}', '{request.POST['lastName']}', " \
                            f"'{request.POST['phoneNumber']}', '{request.POST['email']}', '{request.POST['address']}')"
        execute_query2(insert_non_pemain)

        # Insert into PANITIA table
        insert_panitia = f"INSERT INTO PANITIA (id_panitia, jabatan, username) " \
                         f"VALUES ('{id_panitia}', '{jabatan}', '{username}')"
        execute_query2(insert_panitia)

    except Exception as e:
        error_msg = generate_error_message(e)
        messages.error(request, generate_error_message(e))
        
        return render(request, "register-panitia.html")

    return render(request, "login.html")


def register_penonton(request):
    if request.method == "GET":
        return render(request, "register-penonton.html")

    id_penonton = generate_id()
    username = generate_username(request.POST['firstName'],request.POST['lastName'])  # Generate the username as per your requirements
    password = generate_password()  # Generate the password as per your requirements

    print(f"Username: {username}")
    print(f"Password: {password}")

    try:
        # Insert into USER_SYSTEM table
        insert_user = f"INSERT INTO USER_SYSTEM (username, password) " \
                      f"VALUES ('{username}', '{password}')"
        execute_query2(insert_user)

        # Insert into NON_PEMAIN table
        insert_non_pemain = f"INSERT INTO NON_PEMAIN (id, nama_depan, nama_belakang, nomor_hp, email, alamat) " \
                            f"VALUES ('{id_penonton}', '{request.POST['firstName']}', '{request.POST['lastName']}', " \
                            f"'{request.POST['phoneNumber']}', '{request.POST['email']}', '{request.POST['address']}')"
        execute_query2(insert_non_pemain)

        # Insert into PANITIA table
        insert_penonton = f"INSERT INTO PENONTON (id_penonton, username) " \
                         f"VALUES ('{id_penonton}', '{username}')"
        execute_query2(insert_penonton)

    except Exception as e:
        error_msg = generate_error_message(e)
        messages.error(request, generate_error_message(e))
        
        return render(request, "register-penonton.html")
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
            print(result)

            if result:
                role = "manajer"
                request.session["id_user"] = result[0]['id_manajer']
                
            # role penonton
            query = f"""
            SELECT * FROM penonton
            WHERE username='{username}'
            """
            result = execute_query(query)
            print(result)

            if result:
                role = "penonton"
                request.session["id_user"] = result[0]['id_penonton']
                
            # role panitia
            query = f"""
            SELECT * FROM panitia
            WHERE username='{username}'
            """
            result = execute_query(query)
            print(result)

            if result:
                role = "panitia"
                request.session["id_user"] = result[0]['id_panitia']
            
            request.session["username"] = username
            request.session["password"] = password
            request.session["role"] = role
            print(role, username, password)
            
            return redirect('/dashboard')
    
    return redirect('/login')

@login_required
def dashboard(request):
    print(request.session["id_user"])
    print(request.session["role"])
    print(request.session["username"])
    print(request.session["password"])

    id_user = request.session["id_user"]
    role = request.session["role"]
    
    if role == "manajer":
        #Informasi User
        query = f"""
        SELECT *
        FROM NON_PEMAIN NP 
        JOIN STATUS_NON_PEMAIN SNP ON SNP.id_non_pemain=NP.id
        WHERE id='{id_user}'
        """
        result = execute_query(query)
        print(result)

        context = {
            "user":result,
            "tim":[],
            "pemain":[],
            "pelatih":[]
        }

        #Informasi Tim
        query = f"""
        SELECT *
        FROM TIM_MANAJER TM
        JOIN TIM T ON T.nama_tim=TM.nama_tim
        WHERE id_manajer='{id_user}'
        """
        result = execute_query(query)
        print(result)

        if result:
            context["tim"]+=result
            print(context['tim'][0]['nama_tim'])

            #Informasi Pemain
            query = f"""
            SELECT *
            FROM PEMAIN 
            WHERE nama_tim='{context['tim'][0]['nama_tim']}'
            """
            result = execute_query(query)
            print(result)
            context["pemain"]+=result

            #Informasi Pelatih
            query = f"""
            SELECT *
            FROM PELATIH P
            JOIN NON_PEMAIN NP ON P.id_pelatih=NP.id
            JOIN SPESIALISASI_PELATIH SP ON P.id_pelatih=SP.id_pelatih
            WHERE nama_tim='{context['tim'][0]['nama_tim']}'
            """
            result = execute_query(query)
            print(result)
            context["pelatih"]+=result
        return render(request, 'dashboard-manajer.html', context=context)
    
    elif role == "panitia":
        username = request.session["username"]
        #Informasi User
        query = f"""
        SELECT concat(nama_depan, ' ', nama_belakang) AS nama_lengkap, nomor_hp, email, alamat, jabatan, status
        FROM NON_PEMAIN NP, PANITIA, status_non_pemain
        WHERE id_panitia = id and id_non_pemain = id AND id='{id_user}'
        """
        result = execute_query(query)
        print(result)

        context = {
            "user":result,
            "rapat":[],
        }

        if result:
            query = f"""
            SELECT string_agg(nama_tim, ' vs ') AS tim, s.nama AS nama_stadium, start_datetime
            FROM pertandingan p, tim_pertandingan t, stadium s, rapat r
            WHERE p.id_pertandingan = t.id_pertandingan AND stadium = id_stadium AND p.id_pertandingan = r.id_pertandingan AND perwakilan_panitia = '{id_user}'
            GROUP BY s.nama, start_datetime, end_datetime
            ORDER BY start_datetime;
            """
            result = execute_query(query)
            print(result)
            context["rapat"]+=result

        return render(request, 'dashboard-panitia.html', context=context)
    else:
        username = request.session["username"]
        #Informasi User
        query = f"""
        SELECT concat(nama_depan, ' ', nama_belakang) AS nama_lengkap, nomor_hp, email, alamat, status
        FROM NON_PEMAIN NP, status_non_pemain 
        WHERE id='{id_user}'
        """
        result = execute_query(query)
        print(result)

        context = {
            "user":result,
            "pembelian":[],
        }

        if result:
            query = f"""
            SELECT DISTINCT nomor_receipt, string_agg(nama_tim, ' vs ') AS tim, s.nama AS nama_stadium, start_datetime
            FROM pertandingan p, tim_pertandingan t, stadium s, pembelian_tiket pt
            WHERE p.id_pertandingan = t.id_pertandingan AND stadium = id_stadium AND pt.id_pertandingan = p.id_pertandingan AND id_penonton = '{id_user}'
            GROUP BY nomor_receipt, stadium, start_datetime, end_datetime, s.nama, nomor_receipt
            ORDER BY start_datetime;
            """
            result = execute_query(query)
            print(result)
            context["pembelian"]+=result
        return render(request, 'dashboard-penonton.html', context=context)

@login_required
def logout(request):
    request.session.flush()
    
    return redirect('/')


def generate_id():
    id = str(uuid.uuid4())
    while is_exist_id_non_pemain(id):
        id = str(uuid.uuid4())
    return id

def is_exist_id_non_pemain(id):
    query = f'SELECT id FROM NON_PEMAIN NP WHERE NP.id = \'{id}\''
    lst = execute_query(query)
    return len(lst) > 0

def generate_username(nama_depan,nama_belakang):
    username = f"{nama_depan}{nama_belakang}"
    return username


def generate_password(length=8):
    # Generate a random password of specified length
    characters = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(random.choice(characters) for _ in range(length))
    return password

def generate_error_message(exception):
    msg = str(exception)
    msg = msg[:msg.index('CONTEXT')-1]
    return msg
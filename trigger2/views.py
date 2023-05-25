from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse
from utils.DBUtils import execute_query, commit_query
from utils.decorator import login_required
from datetime import datetime

# Create your views here.
@login_required
def list_peminjaman(request):
    print(request.session["id_user"])
    print(request.session["role"])
    print(request.session["username"])
    print(request.session["password"])

    id_user=request.session["id_user"]

    #Informasi Peminjaman Stadium oleh Manajer
    query = f"""
    SELECT nama, start_datetime
    FROM PEMINJAMAN P
    JOIN STADIUM S ON P.id_stadium=S.id_stadium
    WHERE id_manajer='{id_user}'
    """    
    result = execute_query(query)
    print(result)

    context = {
            "peminjaman":[],
            "error":[],
        }
    
    for i in result:
        context["peminjaman"].append({
            "nama":i["nama"],
            "start_datetime":datetime.strptime(i["start_datetime"], '%Y-%m-%d').strftime("%d %B %Y")
        })
    
    return render(request, 'peminjaman-list.html', context=context)

@login_required
def pesan_stadium(request):
    #List semua stadium
    query = f"""
    SELECT id_stadium, nama
    FROM STADIUM
    """    
    result = execute_query(query)
    print(result)

    context = {
        "stadium":result,
    }

    if request.method == "POST":
        id_stadium=request.POST.get("id_stadium")
        start_date=request.POST.get("date")
        id_manajer = request.session["id_user"]

        #Apakah Update/Insert
        query = f"""
        SELECT COUNT(*)
        FROM PEMINJAMAN
        WHERE id_manajer='{id_manajer}' AND start_datetime='{start_date}'
        """
        result = execute_query(query)
        print(result)

        if result[0]["count"] == 0:
            query = f"""
            INSERT INTO PEMINJAMAN VALUES ('{id_manajer}', '{start_date}', '{start_date}', '{id_stadium}')
            """
        else:
            query = f"""
            UPDATE PEMINJAMAN 
            SET id_stadium='{id_stadium}'
            WHERE id_manajer='{id_manajer}' AND start_datetime='{start_date}'
            """
        try:
            result = commit_query(query)
            print(result)
            return redirect('/peminjaman_stadium/')
        except Exception as e:
            error_msg = generate_error_message(e)
            print(error_msg)
            context['error']=error_msg
            messages.error(request, error_msg)

    return render(request, 'peminjaman-pesan-stadium.html', context=context)

@login_required
def mulai_rapat(request):
    if request.method == 'POST':
        id_pertandingan = request.POST.get('id_pertandingan')
        print(id_pertandingan)
        response = HttpResponseRedirect(reverse('trigger2:isi_rapat'))
        response.set_cookie('id_pertandingan', id_pertandingan)
        print("id pertandingan : " + id_pertandingan)
        return response
    #Informasi Pertandingan yang belum mengadakan Rapat
    query = f"""
    SELECT STRING_AGG(TP.nama_tim, ' vs ') AS tim_tanding, S.nama, P.start_datetime, P.id_pertandingan
    FROM PERTANDINGAN P
    JOIN TIM_PERTANDINGAN TP ON TP.id_pertandingan = P.id_pertandingan
    JOIN STADIUM S ON P.stadium=S.id_stadium
        WHERE p.id_pertandingan NOT IN (
        SELECT id_pertandingan
        FROM rapat
    )
    GROUP BY P.id_pertandingan, S.nama
    """    
    result = execute_query(query)

    context={
        "pertandingan":[]
    }

    for i in result:
        context["pertandingan"].append({
            "tim_tanding":i["tim_tanding"],
            "nama":i["nama"],
            "start_datetime":datetime.strptime(i["start_datetime"], '%Y-%m-%d').strftime("%d %B %Y"),
            "id_pertandingan":i["id_pertandingan"]
        })

    return render(request, 'mulai-rapat.html',context=context)

@login_required
def isi_rapat(request):
    id = request.COOKIES['id_pertandingan']

    # print("id pertandingan" + id)
    query= f"""
    SELECT STRING_AGG(TP.nama_tim, ' vs ') AS tim_tanding
    FROM PERTANDINGAN P
    JOIN TIM_PERTANDINGAN TP ON TP.id_pertandingan = P.id_pertandingan
    WHERE P.id_pertandingan='{id}'
    """
    result = execute_query(query)
    split_result = result[0]['tim_tanding'].split(' vs ')


    tim_a = split_result[0]
    tim_b = split_result[1]
    
    context = {
        'tanding':result[0]
    }

    query=f"""
    SELECT id_manajer
    FROM TIM_MANAJER TM
    WHERE nama_tim='{tim_a}' OR nama_tim='{tim_b}'
    """
    result = execute_query(query)
    print(result)

    rapat_id_manajer_a=result[0]['id_manajer']
    rapat_id_manajer_b=result[1]['id_manajer']

    if request.method == 'POST':
        date_rapat = datetime.now().strftime("%Y-%m-%d")
        isi_rapat = request.POST.get("isi_rapat")
        id_panitia = request.session["id_user"]

        query = f"""
        INSERT INTO RAPAT VALUES ('{id}', '{date_rapat}', '{id_panitia}', '{rapat_id_manajer_a}', '{rapat_id_manajer_b}', '{isi_rapat}')
        """
        result = commit_query(query)

        return redirect('/rapat/mulai')
    
    return render(request, 'isi-rapat.html', context=context) 

def generate_error_message(exception):
    msg = str(exception)
    msg = msg[:msg.index('CONTEXT')-1]
    return msg
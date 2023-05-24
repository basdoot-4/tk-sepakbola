from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import redirect, render
from utils.DBUtils import execute_query
from utils.decorator import login_required
from datetime import datetime

# Create your views here.
def list_peminjaman(request):
    print(request.session["id_user"])
    print(request.session["role"])
    print(request.session["username"])
    print(request.session["password"])

    id_user=request.session["id_user"]

    #Informasi Peminjaman Stadium oleh Manajer
    query = f"""
    SELECT nama, start_datetime, end_datetime
    FROM PEMINJAMAN P
    JOIN STADIUM S ON P.id_stadium=S.id_stadium
    WHERE id_manajer='{id_user}'
    """    
    result = execute_query(query)
    print(result)

    for i in result:
        waktu_selesai = i["end_datetime"][-5:]
        i["end_datetime"] = waktu_selesai

    context = {
        "peminjaman":result,
    }

    return render(request, 'peminjaman-list.html', context=context)

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

    return render(request, 'peminjaman-pesan-stadium.html', context=context)

def pesan_stadium_post(request):
    if request.method == "POST":
        #List semua stadium
        query = f"""
        SELECT nama
        FROM STADIUM
        WHERE id_stadium='{request.POST.get("id_stadium")}'
        """    
        result = execute_query(query)
        print(result[0]['nama'])

        request.session["pesan_nama_stadium"]=result[0]['nama']
        request.session["pesan_id_stadium"]=request.POST.get("id_stadium")
        request.session["pesan_tanggal_stadium"]=request.POST.get("date")
        print(request.session["pesan_tanggal_stadium"])

        return redirect('/peminjaman_stadium/jadwal')
    
    return redirect('/peminjaman_stadium/pesan')

def pesan_waktu(request):
    tgl_pesan = datetime.strptime(request.session["pesan_tanggal_stadium"], '%Y-%m-%d').strftime("%d %B %Y")

    context = {
        "stadium":[request.session["pesan_nama_stadium"]],
        "tanggal":[tgl_pesan]
    }
    return render(request, 'peminjaman-pesan-waktu.html', context=context)

def mulai_rapat(request):
    #Informasi Pertandingan yang belum mengadakan Rapat
    query = f"""
    SELECT STRING_AGG(TP.nama_tim, ' vs ') AS tim_tanding, S.nama, P.start_datetime, P.end_datetime, P.id_pertandingan
    FROM PERTANDINGAN P
    JOIN TIM_PERTANDINGAN TP ON TP.id_pertandingan = P.id_pertandingan
    JOIN STADIUM S ON P.stadium=S.id_stadium
    GROUP BY P.id_pertandingan, S.nama
    """    
    # WHERE id_pertandingan NOT IN (
    #     SELECT id_pertandingan
    #     FROM rapat
    # )
    result = execute_query(query)
    print(result)
    for i in result:
        waktu_selesai = i["end_datetime"][-5:]
        i["end_datetime"] = waktu_selesai

    context={
        "pertandingan":result
    }    

    return render(request, 'mulai-rapat.html',context=context)


def isi_rapat(request,id):
    request.session["rapat_id_pertandingan"]=id
    print(id)
    query= f"""
    SELECT STRING_AGG(TP.nama_tim, ' vs ') AS tim_tanding
    FROM PERTANDINGAN P
    JOIN TIM_PERTANDINGAN TP ON TP.id_pertandingan = P.id_pertandingan
    WHERE P.id_pertandingan='{id}'
    """
    result = execute_query(query)
    split_result = result[0]['tim_tanding'].split(' vs ')
    print(result)

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

    request.session["rapat_id_manajer_a"]=result[0]['id_manajer']
    request.session["rapat_id_manajer_b"]=result[1]['id_manajer']
    
    return render(request, 'isi-rapat.html', context=context) 

def isi_rapat_post(request):
    if request.method == 'POST':
        id_pertandingan = request.session["rapat_id_pertandingan"]
        id_panitia = request.session["user_id"]
        date_rapat = datetime.now
        print(datetime)
        manajer_a = request.session["rapat_id_manajer_a"]
        manajer_b = request.session["rapat_id_manajer_a"]
        isi_rapat = request.POST.get("isi_rapat")
        return redirect('/rapat/mulai')
    return redirect('/rapat/isi')
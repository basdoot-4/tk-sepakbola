from django.shortcuts import render, redirect
from utils.DBUtils import execute_query, commit_query
from django.http import HttpResponseRedirect
from django.urls import reverse

# Create your views here.
def show_pilih_stadium(request):
    if request.method == "POST":
        selected_stadium = request.POST.get("stadium_dipilih")
        selected_date = request.POST.get("date")

        response = HttpResponseRedirect(reverse('trigger_5:show_pilih_pertandingan'))
        response.set_cookie('tiket_stadium', selected_stadium)
        response.set_cookie('tiket_tanggal', selected_date)

        #print(request.session["tiket_tanggal"])
        return response

    context = {
        "stadium":[],
    }

    query = f"""
    SELECT nama
    FROM stadium
    """
    result = execute_query(query)
    print(result)
    context["stadium"]+=result

    return render(request, "pilih_stadium.html", context=context)

def show_pilih_pertandingan(request):
    stadium = request.COOKIES["tiket_stadium"]
    tanggal = request.COOKIES["tiket_tanggal"]

    context = {
        "tima_timb": []
    }

    query = f"""
    SELECT string_agg(nama_tim, ' vs ') AS tim_bertanding, p.id_pertandingan
    FROM pertandingan p, tim_pertandingan t, stadium s
    WHERE p.id_pertandingan = t.id_pertandingan AND stadium = id_stadium AND s.nama = '{ stadium }' AND start_datetime = '{ tanggal }'
    GROUP BY stadium, start_datetime, start_datetime, s.nama, p.id_pertandingan
    """

    result = execute_query(query)
    print(result)

    for i in result:
        split_tim_bertanding = i["tim_bertanding"].split(' vs ')
        print(split_tim_bertanding)
        context["tima_timb"].append({
            "tim_a": split_tim_bertanding[0],
            "tim_b": split_tim_bertanding[1],
            "id_pertandingan": i["id_pertandingan"]
        })

    print(context["tima_timb"])
    return render(request, "pilih_pertandingan.html", context=context)

def show_beli_tiket(request, id):
    context = {
        "error":[],
    }

    if request.method == "POST":
        jenis_tiket = request.POST.get("jenis_tiket_dipilih")
        jenis_pembayaran = request.POST.get("pembayaran_dipilih")
        id_user = request.session["id_user"]
        id_pertandingan = id

        query = f"""
        SELECT COUNT(jenis_tiket)
        FROM pembelian_tiket
        WHERE jenis_tiket = '{ jenis_tiket }'
        GROUP BY jenis_tiket
        """
        result = execute_query(query)
        print(result)

        if(jenis_tiket == "VIP"):
            tiket_receipt = "VIP_" + str(result[0]["count"] + 1)
        elif(jenis_tiket == "Main East"):
            tiket_receipt = "MAE_" + str(result[0]["count"] + 1)
        elif(jenis_tiket == "Kategori 1"):
            tiket_receipt = "KT1_" + str(result[0]["count"] + 1)
        else:
            tiket_receipt = "KT2_" + str(result[0]["count"] + 1)

        print(tiket_receipt)
        print(jenis_tiket)
        print(jenis_pembayaran)
        print(id_user)
        print(id_pertandingan)
        
        query = f"""
        INSERT INTO pembelian_tiket 
        VALUES('{ tiket_receipt }', '{ id_user }', '{ jenis_tiket }', '{ jenis_pembayaran }', '{ id_pertandingan }')
        """
        
        try:
            result = commit_query(query)
            print(result)
            return redirect ('/dashboard')
        except Exception as e:
            error_msg = generate_error_message(e)
            print(error_msg)
            context['error']=error_msg
            #messages.error(request, error_msg)

    return render(request, "beli_tiket.html", context=context)

def generate_error_message(exception):
    msg = str(exception)
    msg = msg[:msg.index('CONTEXT')-1]
    return msg

def show_list_pertandingan(request):
    role = request.session["role"]
    id_user = request.session["id_user"]

    context = {
        "role": [],
        "pertandingan":[],
    }

    context["role"]+=role
    
    if role == "manajer":
        query = f"""
        SELECT string_agg(t.nama_tim, ' vs ') AS tim, s.nama AS nama_stadium, start_datetime AS tanggal_dan_waktu
        FROM pertandingan p, tim_pertandingan t, stadium s, tim_manajer tm
        WHERE p.id_pertandingan = t.id_pertandingan AND stadium = id_stadium AND t.nama_tim = tm.nama_tim 
        AND p.id_pertandingan IN (SELECT id_pertandingan FROM tim_pertandingan tp JOIN tim_manajer tm on tp.nama_tim = tm.nama_tim WHERE id_manajer = '{id_user}')
        GROUP BY stadium, start_datetime, end_datetime, s.nama
        ORDER BY tanggal_dan_waktu;
        """
        result = execute_query(query)
        print(result)
        context["pertandingan"]+=result
        
    else:
        query = f"""
        SELECT string_agg(nama_tim, ' vs ') AS tim, s.nama AS nama_stadium, start_datetime AS tanggal_dan_waktu
        FROM pertandingan p, tim_pertandingan t, stadium s
        WHERE p.id_pertandingan = t.id_pertandingan AND stadium = id_stadium
        GROUP BY stadium, start_datetime, end_datetime, s.nama
        ORDER BY tanggal_dan_waktu;
        """
        result = execute_query(query)
        print(result)
        context["pertandingan"]+=result
    
    return render(request, 'list_pertandingan.html', context=context)

def show_history_rapat(request):
    id_user = request.session["id_user"]

    context = {
        "rapat":[],
    }

    query = f"""
    SELECT string_agg(nama_tim, ' vs ') AS tim, concat(nama_depan, ' ', nama_belakang) AS nama_panitia, s.nama, start_datetime, isi_rapat, p.id_pertandingan
    FROM pertandingan p, tim_pertandingan t, stadium s, rapat r, non_pemain np
    WHERE p.id_pertandingan = t.id_pertandingan AND stadium = id_stadium AND r.id_pertandingan = p.id_pertandingan AND perwakilan_panitia = np.id AND 
    (manajer_tim_a = '{id_user}' OR r.manajer_tim_b = '{id_user}')
    GROUP BY perwakilan_panitia, nama_depan, nama_belakang, s.nama, start_datetime, end_datetime, isi_rapat, p.id_pertandingan
    ORDER BY start_datetime;
    """
    result = execute_query(query)
    print(result)
    context["rapat"]+=result

    return render(request, "history_rapat.html", context=context)
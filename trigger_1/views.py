from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import redirect, render
from utils.DBUtils import execute_query,execute_query2
from utils.decorator import login_required
from datetime import datetime
from django.contrib import messages

# Create your views here.

# Function Page
# Page 1 untuk mendaftarkan Tim
@login_required
def daftarTim(request):    
    id_manajer=request.session["id_user"]

    cek_team = cek_tim_manajer(id_manajer)

    if cek_team:
        return redirect('/kelola-tim')

    if request.method == 'POST':
        nama_tim = request.POST.get('nama_tim')
        universitas = request.POST.get('universitas')
        
        # Membuat Tim Baru
        create_new_team(nama_tim, universitas, id_manajer) 
        
        # Redirect to the next page
        return redirect('/kelola-tim')

    return render(request, 'pendaftaranTim.html')

# Function 2 untuk mengelola Tim
@login_required
def kelola_tim(request):
    id_manajer = request.session["id_user"]
    nama_tim = get_tim_manajer(id_manajer)
    print("id_manajer:" + id_manajer)

    cek_team = cek_tim_manajer(id_manajer)

    if cek_team != True:
        return redirect('/daftar-tim')
    

    # Query 1 untuk mengambil semua pemain yang memiliki tim sama dengan manajer
    query_pemain = f"""
    SELECT *
    FROM PEMAIN
    WHERE nama_tim IN (
        SELECT nama_tim
        FROM TIM_MANAJER
        WHERE id_manajer = '{id_manajer}'
    )
    """
    list_pemain = execute_query(query_pemain)

    # Query 2 untuk mengambil semua pelatih yang memiliki tim sama dengan manajer
    query_pelatih = f"""
    SELECT N.nama_depan, N.nama_belakang, N.nomor_hp, N.email, N.alamat, SP.spesialisasi, PL.id_pelatih
    FROM PELATIH AS PL
    JOIN NON_PEMAIN AS N ON PL.id_pelatih = N.id
    JOIN SPESIALISASI_PELATIH AS SP ON PL.id_pelatih = SP.id_pelatih
    WHERE PL.nama_tim IN (
        SELECT T.nama_tim
        FROM TIM_MANAJER AS TM
        JOIN TIM AS T ON TM.nama_tim = T.nama_tim
        WHERE TM.id_manajer = '{id_manajer}'
    )
    """
    list_pelatih = execute_query(query_pelatih)

    context = {
        "nama_tim": nama_tim,
        "list_pemain": list_pemain,
        "list_pelatih": list_pelatih
    }

    return render(request, 'kelolaTim.html', context=context)

# Function 3 untuk mendaftarkan pemain/pelatih
@login_required
def daftar_pemain_pelatih(request):

    id_manajer = request.session["id_user"]
    nama_tim = get_tim_manajer(id_manajer)

    # Query untuk mengambil pemain/pelatih yang tidak berada di suatu tim (team = null)
    query_pemain = """
    SELECT *
    FROM PEMAIN
    WHERE nama_tim IS NULL
    """
    query_pelatih = """
    SELECT N.nama_depan, N.nama_belakang, SP.Spesialisasi, PL.id_pelatih
    FROM PELATIH AS PL
    JOIN NON_PEMAIN AS N ON PL.id_pelatih = N.id
    JOIN SPESIALISASI_PELATIH AS SP ON PL.id_pelatih = SP.id_pelatih
    WHERE PL.nama_tim IS NULL;
    """
    list_pemain_tersedia = execute_query(query_pemain)
    list_pelatih_tersedia = execute_query(query_pelatih)

    context = {
        'nama_tim': nama_tim,
        'list_pemain': list_pemain_tersedia,
        'list_pelatih': list_pelatih_tersedia
    }

    return render(request, 'daftarPemainDanPelatih.html', context=context)

# Util Function
# Function 1 untuk cek apakah manajer punya tim atau belum
def cek_tim_manajer(id_manajer):
    query = f"""
    SELECT COUNT(*)
    FROM TIM_MANAJER
    WHERE TIM_MANAJER.id_manajer = '{id_manajer}'
    """
    result = execute_query(query)
    count = result[0]['count']
    return count > 0

# Function 2 untuk membuat sebuah tim baru
def create_new_team(nama_tim, universitas, id_manajer):
    query = f"""
    INSERT INTO TIM (nama_tim, universitas)
    VALUES ('{nama_tim}', '{universitas}')
    """
    execute_query(query)
    
    query = f"""
    INSERT INTO TIM_MANAJER (id_manajer, nama_tim)
    VALUES ('{id_manajer}', '{nama_tim}')
    """
    execute_query(query)

# Function 2 untuk mengambil nama tim manajer
def get_tim_manajer(id_manajer):
    query = f"""
    SELECT nama_tim
    FROM TIM_MANAJER
    WHERE id_manajer = '{id_manajer}'
    """

    result = execute_query(query)
    nama_tim = result[0]['nama_tim']
    return nama_tim

# Function 3 untuk membuat pemain jadi kapten
def make_captain(request, id_pemain):
    query = f"""
    UPDATE PEMAIN
    SET is_captain = TRUE
    WHERE id_pemain = '{id_pemain}'
    """
    execute_query(query)
    return redirect('/kelola-tim')

# Function 4 untuk menghapus pemain dari tim
def remove_player(request, id_pemain):
    query = f"""
    UPDATE PEMAIN
    SET nama_tim = NULL
    WHERE id_pemain = '{id_pemain}'
    """
    execute_query2(query)
    return redirect('/kelola-tim')

# Function 5 untuk menghapus pelatih dari tim
def remove_coach(request, id_pelatih):
    query = f"""
    UPDATE PELATIH
    SET nama_tim = NULL
    WHERE id_pelatih = '{id_pelatih}'
    """
    execute_query2(query)
    return redirect('/kelola-tim')

# Function 6 untuk mendaftarkan pemain
def submit_pemain(request):

    id_manajer = request.session["id_user"]
    nama_tim = get_tim_manajer(id_manajer)

    if request.method == 'POST':
        id_pemain = request.POST.get('playerDropdown')
        print(id_pemain)
        query = f"""
        UPDATE PEMAIN
        SET nama_tim = '{nama_tim}'
        WHERE id_pemain = '{id_pemain}'
        """
        execute_query2(query)
        return redirect('/kelola-tim')

# Function 7 untuk mendaftarkan pelatih
def submit_pelatih(request):
    id_manajer = request.session["id_user"]
    nama_tim = get_tim_manajer(id_manajer)
    if request.method == 'POST':
        id_pelatih = request.POST.get('pelatihDropdown')
        print(id_pelatih)
        query = f"""
        UPDATE PELATIH
        SET nama_tim = '{nama_tim}'
        WHERE id_pelatih = '{id_pelatih}'
        """
        try:
            execute_query2(query)
            messages.success(request, f"Berhasil menambahkan pelatih")
            return redirect('/kelola-tim')
        except Exception as e:
            messages.error(request, generate_error_message(e))
            print(generate_error_message(e))
            return redirect('/kelola-tim')
    
# Function 8 untuk ambil error message buat trigger
def generate_error_message(exception):
    msg = str(exception)
    msg = msg[:msg.index('CONTEXT')-1]
    return msg
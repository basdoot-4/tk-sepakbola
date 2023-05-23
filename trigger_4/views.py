from django.shortcuts import render
from utils.decorator import login_required
from utils.DBUtils import execute_query

# Create your views here.
@login_required
def manage(request):
    
    return render(request, 'manage-pertandingan.html')

def get_stage_1(request):
    query="""select p.id_pertandingan, 
            string_agg(tp.nama_tim, ' vs ' order by tp.nama_tim) as tim,
            p.start_datetime
            from pertandingan p,
                tim_pertandingan tp
            where tp.id_pertandingan = p.id_pertandingan
            group by p.id_pertandingan, p.start_datetime
            order by p.start_datetime asc
    """
    result = execute_query(query)
    
    context = {"tabel_1" : []}
    for i in range(len(result)):
        context['tabel_1'].append({
            'number': i+1,
            'id_pertandingan' : result[i]['id_pertandingan'],
            'tim' : result[i]['tim'],
            'tim_1': (result[i]['tim']).split(' vs ')[0],
            'tim_2': (result[i]['tim']).split(' vs ')[1],
            'waktu': result[i]['start_datetime']
        })
    return render(request, 'manage-pertandingan.html', context=context)

def start(request, id):
    query = f"""select tp.nama_tim as tim
               from tim_pertandingan tp
               where tp.id_pertandingan = '{id}'
               order by tim asc
    """
    result = execute_query(query)
    
    context = {
        'id_pertandingan' : id,
        'tim_1' : result[0]['tim'],
        'tim_2' : result[1]['tim']
    }
    return render(request, 'mulai-pertandingan.html', context)

def get_peristiwa(request, id, name):
    peristiwa = []
    query = f"""
    SELECT p.jenis, 
           CONCAT(m.nama_depan, ' ', m.nama_belakang) as nama_pemain,
           datetime
    FROM peristiwa p,
         pemain m
    WHERE p.id_pertandingan = '{id}'
          AND m.id_pemain = p.id_pemain
          AND m.nama_tim = '{name}'
    """
    result = execute_query(query)
    
    for i in range(len(result)):
        peristiwa.append({
            'number': i+1,
            'jenis' : result[i]['jenis'],
            'nama_pemain' : result[i]['nama_pemain'],
            'waktu' : result[i]['datetime']
        })
    
    context = {
        'tim' : name,
        'peristiwa': peristiwa
    }
    return render(request, 'lihat-peristiwa.html', context)

def current_peristiwa(request, id, name):
    # get previous inserts
    previous_inserts = []
    query = f"""
    SELECT p.jenis, 
           CONCAT(m.nama_depan, ' ', m.nama_belakang) as nama_pemain,
           datetime
    FROM peristiwa p,
         pemain m
    WHERE p.id_pertandingan = '{id}'
          AND m.id_pemain = p.id_pemain
          AND m.nama_tim = '{name}'
    """
    result = execute_query(query)
    
    for i in range(len(result)):
        previous_inserts.append({
            'jenis' : result[i]['jenis'],
            'nama_pemain' : result[i]['nama_pemain'],
            'waktu' : result[i]['datetime']
        })
    
    # get data pemain
    data_pemain = []
    query = f"""select id_pemain, concat(nama_depan, ' ', nama_belakang) as nama_pemain
                from pemain
                where nama_tim = '{name}'"""
    data = execute_query(query)
    
    for i in range(len(data)):
        data_pemain.append({
            'id_pemain' : data[i]['id_pemain'],
            'nama_pemain' : data[i]['nama_pemain'],
        })
    
    context = {
        'id_pertandingan' : id,
        'tim' : name,
        'peristiwa' : previous_inserts,
        'data_pemain' : data_pemain
    }
    return render(request, 'catat-peristiwa.html', context)

def add_peristiwa(request, id, name):
    if request.method == "POST":
        nama_pemain = request.POST.get("nama-pemain")
        peristiwa = request.POST.get("peristiwa")
        waktu = request.POST.get("waktu")
        
        # get id pemain
        query = f"""INSERT INTO PERISTIWA()
        """
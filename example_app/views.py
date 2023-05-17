from django.shortcuts import render
from utils.DBUtils import execute_query

def index(request):
    query = """
    SELECT p.id_pertandingan, p.datetime, p.jenis, p.id_pemain
    FROM peristiwa p
    """
    result = execute_query(query)
    print(result[0])
    
    context = {"peristiwa":[]}
    
    for i in range(len(result)):
        context['peristiwa'].append({
            'id_pertandingan': result[i]['id_pertandingan'],
            'datetime': result[i]['datetime'], 
            'jenis': result[i]['jenis'], 
            'id_pemain': result[i]['id_pemain']
        })
    return render(request, 'index.html', context=context)

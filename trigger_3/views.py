from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseRedirect
from django.db import connection
from django.views.decorators.csrf import csrf_exempt
from utils.decorator import login_required
from datetime import datetime
from utils.DBUtils import execute_query, commit_query

@login_required
def pembuatanPertandingan(request, id_pertandingan, begin_datetime, end_datetime, id_stadium) :
    if request.method == "POST":
        id_pertandingan = request.POST.get("id_pertandingan")
        begin_datetime = request.POST.get("begin_datetime")
        end_datetime = request.POST.get("end_datetime")
        id_stadium = request.POST.get("id_stadium")
        
        query = f"""INSERT INTO PERTANDINGAN (id_pertandingan, datetime, datetime, id_stadium)
                    VALUES ('{id_pertandingan}', '{begin_datetime}', '{end_datetime}', '{id_stadium}')
        """
        
        with connection.cursor() as cursor:
            cursor.execute(query)
        
        return redirect('')

    

@login_required
def list_all_Pertandingan(request) :
    role = request.session["role"]


    context = {
        "role": [],
        "pertandingan":[],
    }

    context["role"].append(role)

    print("role aku: " + context["role"][0])

    if role == "panitia":
        query = f"""
        SELECT * FROM PERTANDINGAN ;
        """
        result = execute_query(query)
        # print(result)
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
    
    return render(request, 'list-pertandingan.html', context=context)

@login_required
def updatePertandingan(request, id_pertandingan, begin_datetime, end_datetime, id_stadium) :
    if request.method == "POST":
        id_pertandingan = request.POST.get("id_pertandingan")
        begin_datetime = request.POST.get("begin_datetime")
        end_datetime = request.POST.get("end_datetime")
        id_stadium = request.POST.get("id_stadium")

        
        query = f"""UPDATE PERTANDINGAN SET begin_datetime = {begin_datetime}, end_datetime = {end_datetime}, stadium = {id_stadium} WHERE PERTANDINGAN.id_pertandingan = {id_pertandingan}')"""
        
        with connection.cursor() as cursor:
            cursor.execute(query)
        
        return redirect('')

@login_required
def deletePertandingan(request, id_pertandingan) :
     if request.method == "POST":
        id_pertandingan = request.POST.get("id_pertandingan")

        
        query = f"""DELETE FROM PERTANDINGAN WHERE PERTANDINGAN.id_pertandingan = {id_pertandingan}')"""
        
        with connection.cursor() as cursor:
            cursor.execute(query)
        
        return redirect('')


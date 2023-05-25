from django.urls import path
from trigger_5.views import *

app_name = 'trigger_5'

urlpatterns = [
    path('pilih-stadium', show_pilih_stadium, name='show_pilih_stadium'),
    path('pilih-pertandingan', show_pilih_pertandingan, name='show_pilih_pertandingan'),
    path('beli-tiket/<str:id>', show_beli_tiket, name='show_beli_tiket'),
    path('list-pertandingan', show_list_pertandingan, name='show_list_pertandingan'),
    path('history-rapat', show_history_rapat, name='show_history_rapat'),
]
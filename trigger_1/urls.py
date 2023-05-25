from django.urls import path
from trigger_1.views import *

app_name = 'trigger_1'

urlpatterns = [
    path('daftar-tim', daftarTim, name='daftar-tim'),
    path('kelola-tim',kelola_tim, name='kelola-tim'),
    path('daftar-pemain-pelatih',daftar_pemain_pelatih, name='daftar-pemain-pelatih'),
    path('make-captain/<int:id_pemain>/',make_captain, name='make_captain'),
    path('remove_player/<int:id_pemain>/',remove_player, name='remove_player'),
    path('remove_coach/<int:id_pelatih>/',remove_coach,name='remove_coach'),
    path('submit-pemain/', submit_pemain, name='submit_pemain'),
    path('submit-pelatih/', submit_pelatih, name='submit_pelatih'),
]
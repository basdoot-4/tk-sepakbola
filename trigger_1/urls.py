from django.urls import path
from trigger_1.views import *

app_name = 'trigger_1'

urlpatterns = [
    path('daftar-tim', daftarTim, name='daftar-tim'),
    path('kelola-tim',kelola_tim, name='kelola-tim'),
    path('daftar-pemain-pelatih',daftar_pemain_pelatih, name='daftar-pemain-pelatih')
]
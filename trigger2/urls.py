from django.urls import path
from trigger2.views import *

app_name = 'trigger2'

urlpatterns = [
    path('peminjaman_stadium/', list_peminjaman, name='list_peminjaman'),
    path('peminjaman_stadium/pesan', pesan_stadium, name='pesan_stadium'),
    path('rapat/mulai', mulai_rapat, name='mulai_rapat'),
    path('rapat/isi', isi_rapat, name='isi_rapat')
]
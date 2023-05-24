from django.urls import path
from trigger2.views import *

app_name = 'trigger2'

urlpatterns = [
    path('peminjaman_stadium/', list_peminjaman, name='list_peminjaman'),
    path('peminjaman_stadium/pesan', pesan_stadium, name='pesan_stadium'),
    path('peminjaman_stadium/pesan_post', pesan_stadium_post, name='pesan_stadium_post'),
    path('peminjaman_stadium/jadwal', pesan_waktu, name='pesan_waktu'),
    path('rapat/mulai', mulai_rapat, name='mulai_rapat'),
    path('rapat/isi/<str:id>', isi_rapat, name='isi_rapat'),
    path('rapat/isi/post', isi_rapat_post, name='isi_rapat_post'),
]
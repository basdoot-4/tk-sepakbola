from django.urls import path
from trigger_4.views import *

app_name = 'trigger_4'

urlpatterns = [
    path('manage-tes', manage, name='manage'),
    path('manage', get_stage_1, name='get_stage_1'),
    path('mulai/<str:id>', start, name='start'),
    path('peristiwa/<str:id>/<str:name>', get_peristiwa, name='get_peristiwa'),
    path('catat/<str:id>/<str:name>', current_peristiwa, name='current_peristiwa'),
    path('tambah/<str:id>/<str:name>', add_peristiwa, name='add_peristiwa'),
    path('delete/<str:id>/<str:name>/<str:waktu>', delete_peristiwa, name='delete_peristiwa'),
]
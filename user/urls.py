from django.urls import path
from user.views import *

app_name = 'user'

urlpatterns = [
    path('dashboard/', dashboard_manajer, name='dashboard-manajer'),
]
from django.urls import path
from user.views import *

app_name = 'user'

urlpatterns = [
    path('', index, name='index'),
    path('login/', login, name='login'),
    path('logout/', logout, name='logout'),
    path('login/post/', login_post, name='login_post'),
    path('register/', register, name='register'),
    path('register/manajer', register_manajer, name='register_manajer'),
    path('register/panitia', register_panitia, name='register_panitia'),
    path('register/penonton', register_penonton, name='register_penonton'),
    path('dashboard/', dashboard, name='dashboard'),
]
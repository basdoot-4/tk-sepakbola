from django.shortcuts import render

# Create your views here.
def dashboard_manajer(request):
    return render(request, 'dashboard-penonton.html')
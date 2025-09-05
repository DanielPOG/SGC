from django.shortcuts import render

def autorizaciones(request):
    return render(request, 'layout/autorizaciones.html')

def user_autorizado(request):
    return render(request, 'pages/user_autorizado.html')

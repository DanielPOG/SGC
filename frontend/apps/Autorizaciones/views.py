from django.shortcuts import render

def autorizaciones(request):
    return render(request, 'layout/autorizaciones.html')

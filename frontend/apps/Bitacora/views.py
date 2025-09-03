from django.shortcuts import render

def bitacora(request):
    return render(request, 'layout/bitacora.html')

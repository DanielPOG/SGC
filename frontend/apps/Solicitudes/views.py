from django.shortcuts import render

def solicitudes(request):
    return render(request, 'layout/solicitudes.html')

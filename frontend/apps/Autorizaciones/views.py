from django.shortcuts import render

# Create your views here.
def autorizaciones(request):
    return render(request, 'layout/autorizaciones.html')
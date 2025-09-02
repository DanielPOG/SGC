from django.shortcuts import render

# Create your views here.
def id_planta(request):
    return render(request, 'pages/id_planta.html')

def crear_idp(request):
    return render(request, 'pages/crear_idp.html')
from django.shortcuts import render

# Create your views here.
def id_planta(request):
    return render(request, 'layout/id_planta.html')
def newid_palnta(request):
    return render(request, 'pages/newid_planta.html')


def asignar_idp(request):
    return render(request, 'pages/asignar_idp.html')

def editar_asig_idp(request):
    return render(request, 'pages/editar_asig_idp.html')

def editar_idp(request):
    return render(request, 'pages/editar_idp.html')
from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request, 'layout/index.html')

def newcargo(request):
    return render(request, 'pages/newcargo.html')

def cargohistorial(request):
    return render(request, 'pages/cargohistorial.html')
def nuevo_fc(request):
    return render(request, 'pages/nuevo_fc.html')

def cargoIndex(request):
    return render(request, 'layout/cargo.html')

def editar_cargo(request):
    return render(request, 'pages/editar_cargo.html')

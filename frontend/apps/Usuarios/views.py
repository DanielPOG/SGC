from django.shortcuts import render

# Create your views here.
# Autenticación
def login_view(request):
    return render(request, 'pages/login.html')

# Layout general
def index(request):
    return render(request, 'layout/index.html')

# 👤 Páginas de usuario
def funcionario(request):
    return render(request, 'pages/funcionario.html')

def cargo(request):
    return render(request, 'pages/cargo.html')

def grupo_sena(request):
    return render(request, 'pages/grupo_sena.html')

def id_planta(request):
    return render(request, 'pages/id_planta.html')

def solicitudes(request):
    return render(request, 'pages/solicitudes.html')

def autorizaciones(request):
    return render(request, 'pages/autorizaciones.html')

def bitacora(request):
    return render(request, 'pages/bitacora.html')

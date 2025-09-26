from django.shortcuts import render
from django.contrib.auth import logout
from django.shortcuts import redirect
# Create your views here.


def index(request):
    return render(request, 'layout/index.html', {
        'usuario': request.user
    })

def login_view(request):
    return render(request, 'pages/login.html')

def sidebar(request):
    return render(request, 'layout/sidebar.html')

def pr(request):
    return render(request, 'layout/pr.html')

# DEF usuario paginas
def funcionario(request):
    return render(request, 'pages/funcionario.html')


def cargo(request):
    return render(request, 'layout/cargo.html')

def grupo_sena(request):
    return render(request, 'pages/grupo_sena.html')

def reportes(request):
    return render(request, 'layout/reportes.html')

def id_planta(request):
    return render(request, 'pages/id_planta.html')

def solicitudes(request):
    return render(request, 'layout/solicitudes.html')

def funcionario(request):
    return render(request, 'layout/funcionario.html')

def newfuncionario(request):
    return render(request, 'pages/newfuncionario.html')

def historial_funcionario(request):
    return render(request, 'pages/historial_funcionario.html')

def datos_basicosfun(request):
    return render(request, 'pages/datos_basicosfun.html')

def cargo_actualfun(request):
    return render(request, 'pages/cargo_actualfun.html')


def cargos_anterioresfun(request):
    return render(request, 'pages/cargos_anterioresfun.html')

def estudios_fun(request):
    return render(request, 'pages/estudios_fun.html')

def editar_fun(request):
    return render(request, 'pages/editar_fun.html')

def pr(request):
    return render(request, 'layout/pr.html')

def prContet(request):
    return render(request, 'pages/prContent.html')

#  cierra sesion 
def logout_view(request):
    logout(request)
    return redirect('login') # o la URL de tu página de login


from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response


from rest_framework.decorators import api_view, permission_classes
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def usuario_actual(request):
    user = request.user
    return Response({
        "id": user.id,
        "nombre": user.first_name or user.username,
        "correo": user.email,
        "rol": getattr(user, "rol", None)  # Si tienes un campo rol
    })


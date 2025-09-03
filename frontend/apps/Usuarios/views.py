from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request, 'layout/index.html')
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
    return render(request, 'pages/reportes.html')

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



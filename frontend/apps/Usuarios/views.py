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
    return render(request, 'pages/cargo.html')

def grupo_sena(request):
    return render(request, 'pages/grupo_sena.html')

def reportes(request):
    return render(request, 'pages/reportes.html')

def id_planta(request):
    return render(request, 'pages/id_planta.html')

def solicitudes(request):
    return render(request, 'pages/solicitudes.html')

def newcargo(request):
    return render(request, 'pages/newcargo.html')

def cargohistorial(request):
    return render(request, 'pages/cargohistorial.html')
def nuevo_fc(request):
    return render(request, 'pages/nuevo_fc.html')




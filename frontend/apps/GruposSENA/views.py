from django.shortcuts import render

# Create your views here.
def grupo_sena(request):
    return render(request, 'layout/grupo_sena.html')

def new_grupo(request):   
    return render(request, 'pages/new_grupo.html')

def historial_grupo(request):   
    return render(request, 'pages/historial_grupo.html')
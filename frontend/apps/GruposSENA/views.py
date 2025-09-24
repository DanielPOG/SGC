from django.shortcuts import render, get_object_or_404


def grupo_sena(request):
    return render(request, 'layout/grupo_sena.html')

def new_grupo(request):
    return render(request, 'pages/new_grupo.html')

def historial_grupo(request):
    return render(request, 'pages/historial_grupo.html')
 
def editar_grupo(request, id):
    return render(request, 'pages/editar_grupo.html', {"mode": "edit", "grupo": id})

def grupo_update(request, id):
    return render(request, 'pages/editar_grupo.html', {"mode": "edit", "grupo": id})
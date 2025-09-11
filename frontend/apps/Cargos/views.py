from django.contrib import messages
from django.shortcuts import render, redirect

# Create your views here.
def index(request):
    return render(request, 'layout/index.html')

def newcargo(request):
    return render(request, 'pages/newcargo.html', {"mode": "create"})

def cargohistorial(request):
    return render(request, 'pages/cargohistorial.html')
def nuevo_fc(request):
    return render(request, 'pages/nuevo_fc.html')

def cargoIndex(request):
    if request.GET.get("created"): # si el parametro created esta en la url agrega el mensaje de exito
        messages.success(request, "Cargo creado con éxito ") # agrega mensaje de exito
        return redirect("cargoIndex")  # redirige sin parametros al index

    if request.GET.get("updated"): # si el parametro updated esta en la url agrega el mensaje de exito
        messages.success(request, "Cargo actualizado con éxito ") # agrega mensaje de exito
        return redirect("cargoIndex")  # redirige sin parámetros

    return render(request, 'layout/cargo.html')

def editar_cargo(request, id):
    return render(request, 'pages/newcargo.html',  {"mode": "edit", "cargo_id": id})

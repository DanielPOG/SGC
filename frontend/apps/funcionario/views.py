from django.shortcuts import render

# Create your views here.

def menu(request):
    return render(request, 'layout/menu.html')

def cambiar_contra(request):
    return render(request, 'pages/cambiar_contra.html')

def actualizar_datos(request):
    return render(request, 'pages/actualizar_datos.html')

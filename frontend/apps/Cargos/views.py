from django.shortcuts import render

def cargo(request):
    return render(request, 'layout/cargo.html')

def newcargo(request):
    return render(request, 'pages/newcargo.html')

def cargohistorial(request):
    return render(request, 'pages/cargohistorial.html')
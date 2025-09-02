from django.shortcuts import render

# Create your views here.
def solicitudes(request):
    return render(request, 'layout/solicitudes.html')

def todas_solicitudes(request):
    return render(request, 'pages/todas_solicitudes.html')

def solicitud_pendiente(request):    
    return render(request, 'pages/solicitud_pendiente.html')

def solicitud_revicion(request):
    return render(request, 'pages/solicitud_revicion.html')

def solicitud_aprovada(request):
    return render(request, 'pages/solicitud_aprovada.html')

def estado_solucitud(request):
    return render(request, 'layout/estado_solicitud.html')


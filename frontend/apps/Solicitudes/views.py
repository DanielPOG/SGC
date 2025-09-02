from django.shortcuts import render

# Create your views here.
def solicitudes(request):
    return render(request, 'layout/solicitudes.html')

def todas_solicitudes(request):
    return render(request, 'pages/todas_solicitudes.html')


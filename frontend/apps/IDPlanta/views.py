from django.shortcuts import render

# Create your views here.
def id_planta(request):
    return render(request, 'layout/id_planta.html')
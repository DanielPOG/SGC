from django.shortcuts import render

# Create your views here.
def id_planta(request):
    return render(request, 'layout/id_planta.html')
def newid_palnta(request):
    return render(request, 'pages/newid_planta.html')

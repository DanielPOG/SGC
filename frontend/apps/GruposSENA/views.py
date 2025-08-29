from django.shortcuts import render

# Create your views here.
def grupo_sena(request):
    return render(request, 'layout/grupo_sena.html')
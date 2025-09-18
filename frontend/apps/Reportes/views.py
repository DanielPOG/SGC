from django.shortcuts import render

def reportes(request):
    return render(request, 'layout/reportes.html')

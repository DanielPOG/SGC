from django.shortcuts import render


def menu(request):
    return render(request, 'layout/menu.html')

def userfuncionario(request):   
    return render(request, 'pages/userfuncionario.html')



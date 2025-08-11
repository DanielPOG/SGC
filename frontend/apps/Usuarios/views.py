from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request, 'layout/index.html')
def login_view(request):
    return render(request, 'pages/login.html')
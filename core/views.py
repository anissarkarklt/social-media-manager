from django.shortcuts import render

# Create your views here.
def dashboard(request):
    return render(request,'core/index.html')
def login(request):
    return render(request,'core/login.html')
def register(request):
    return render(request,'core/register.html')
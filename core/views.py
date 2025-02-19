from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, logout
from django.contrib.auth import login as auth_login  # Use alias to avoid conflicts
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages
from .forms import CustomUserCreationForm
from .forms import CustomLoginForm
from django.http import HttpResponse
from django.db import connection  # Import connection
# Create your views here.
def dashboard(request):
    return render(request,'core/index.html')
def login_view(request):
    if request.method == 'POST':
        form = CustomLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                auth_login(request, user)
                return redirect('login')  # Replace 'home' with your desired URL name
            else:
                messages.error(request, 'Invalid username or password.')
    else:
        form = CustomLoginForm()
    
    return render(request, 'core/login.html', {'loginForm': form})

def register_view(request):
    return render(request, 'core/register.html')
def register_submit(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # auth_login(request, user)  # Use the imported alias
            return redirect('dashboard')  # Ensure 'dashboard' is defined in your urls.py
            connection.close()
            # return HttpResponse(form)
        else:
            return HttpResponse(f"Form Errors: {form.errors}")

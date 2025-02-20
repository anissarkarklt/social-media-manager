from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, logout
from django.contrib.auth import login as auth_login  # Use alias to avoid conflicts
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages
from .forms import CustomUserCreationForm
from .forms import CustomLoginForm
from django.http import HttpResponse
from django.db import connection  # Import connection
from django.db import IntegrityError, transaction
from django.contrib.auth.models import User

# Create your views here.
def dashboard(request):
    return render(request,'core/index.html')
def login_view(request):
    if request.method == 'POST':
        form = CustomLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            
            if user is not None:
                auth_login(request, user)
                return redirect('dashboard')  # Replace 'home' with your desired URL name
            else:
                messages.error(request, 'Invalid username or password.')
    else:
        form = CustomLoginForm()
    
    return render(request, 'core/login.html', {"form": form })


def register_view(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()  # Save the user with all fields
            auth_login(request, user)  # Log the user in
            return redirect("dashboard")  # Redirect to a success page
    else:
        form = CustomUserCreationForm()

    return render(request, "core/register.html", {"form": form})

def register_submit(request):
    # This handles the form submission from your template
    return register_view(request)
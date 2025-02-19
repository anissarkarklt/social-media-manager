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
            username = form.cleaned_data.get('username')

            try:
                with transaction.atomic():  # Ensures data is committed properly
                    if User.objects.filter(username=username).exists():
                        return HttpResponse("Error: Username already exists!", status=400)

                    user = form.save()  # Save the user only if it doesn't exist
                    connection.close()  # Ensure DB connection is closed
                    return redirect('dashboard')

            except IntegrityError as e:
                return HttpResponse(f"Database Error: {str(e)}", status=400)

        else:
            return HttpResponse(f"Form Errors: {form.errors}", status=400)

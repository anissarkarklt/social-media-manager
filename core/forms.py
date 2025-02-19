from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class CustomUserCreationForm(UserCreationForm):
    # Create a custom field for "name" that will be mapped to the User model's username.
    name = forms.CharField(
        max_length=150, 
        required=True, 
        label="Name",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your name'})
    )
    
    # You can also customize the email widget if needed.
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter your email'})
    )
    
    class Meta:
        model = User
        # Use the custom 'name' field in the form but map it to username when saving.
        fields = ("email", "name", "password1", "password2")
    
    def save(self, commit=True):
        # Get the user object from the parent form
        user = super().save(commit=False)
        # Map the custom 'name' field to the User model's 'username' field.
        user.username = self.cleaned_data["name"]
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user
    
    # Optionally remove widget attributes if you want to fully customize in HTML.
class CustomLoginForm(forms.Form):
    username = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'})
    )
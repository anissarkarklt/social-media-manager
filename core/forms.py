from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.contrib.auth import authenticate

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        label="Email",
        widget=forms.EmailInput(attrs={"placeholder": "Email here..."}),
    )
    first_name = forms.CharField(
        required=False,
        label="First Name",
        widget=forms.TextInput(attrs={"placeholder": "First Name here..."}),
    )
    last_name = forms.CharField(
        required=False,
        label="Last Name",
        widget=forms.TextInput(attrs={"placeholder": "Last Name here..."}),
    )
    password1 = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={"placeholder": "Password here..."}),
    )
    password2 = forms.CharField(
        label="Repeat Password",
        widget=forms.PasswordInput(attrs={"placeholder": "Repeat Password here..."}),
    )
    terms = forms.BooleanField(
        required=True,
        label="Accept our Terms and Conditions",
    )

    class Meta:
        model = User
        fields = ("email", "first_name", "last_name", "password1", "password2")

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if User.objects.filter(email=email).exists():
            raise ValidationError("This email is already registered.")
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.username = self.cleaned_data["email"]  # Use email as the username
        user.first_name = self.cleaned_data["first_name"]
        user.last_name = self.cleaned_data["last_name"]
        if commit:
            user.save()
        return user
class CustomLoginForm(forms.Form):
    email = forms.EmailField(
        required=True,
        label="Email",
        widget=forms.EmailInput(attrs={"placeholder": "Email here..."}),
    )
    password = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={"placeholder": "Password here..."}),
    )
    terms = forms.BooleanField(
        required=True,
        label="Accept our Terms and Conditions",
    )
    def clean_email(self):
        email = self.cleaned_data.get("email")
        if email:
            try:
                user = User.objects.get(email=email)  # Get user by email
            except User.DoesNotExist:
                raise ValidationError("User does not exist.")
        return email
    def clean_password(self):
        email = self.cleaned_data.get("email")
        password = self.cleaned_data.get("password")

        if email and password:
            try:
                user = User.objects.get(email=email)  # Get user by email
            except User.DoesNotExist:
                raise ValidationError("User does not exist.")  # Error if email is not found

            authenticated_user = authenticate(username=user.username, password=password)
            if authenticated_user is None:
                raise ValidationError("Incorrect password.")  # Error if password is wrong

        return password
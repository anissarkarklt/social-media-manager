from django.contrib.auth.views import LogoutView
from django.urls import path
from . import views

urlpatterns = [
    path('',views.login_view,name='login'),
    path('register/',views.register_view,name='register'),
    path('register-submit/',views.register_submit,name='register_submit'),
    path('dashboard/',views.dashboard,name='dashboard'),
    path("logout/", LogoutView.as_view(next_page="login"), name="logout"),
]
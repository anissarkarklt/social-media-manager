from django.urls import path
from . import views

urlpatterns = [
    path('',views.register_view,name='register'),
    path('register-submit/',views.register_submit,name='register_submit'),
    path('dashboard/',views.dashboard,name='dashboard'),
]
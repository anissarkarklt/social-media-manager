from django.shortcuts import render

# Create your views here.
def home(request):
    posts = 'welcome'
    return render(request,'social_api/welcome.html',{'posts':posts})
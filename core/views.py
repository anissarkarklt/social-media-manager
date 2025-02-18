from django.shortcuts import render

# Create your views here.
def welcome(request):
    posts = 'welcome'
    return render(request,'core/welcome.html',{'posts':posts})
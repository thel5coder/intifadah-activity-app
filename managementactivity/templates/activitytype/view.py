from django.shortcuts import render, redirect

def index(request):
    return render(request,'activitytype/list.html')

def create(request):
    return render(request,'activitytype/create.html')
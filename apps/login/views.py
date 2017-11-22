from __future__ import unicode_literals
from django.shortcuts import render, redirect, HttpResponse
from django.contrib import messages
from .models import User
from datetime import datetime

# Create your views here.

def index(request):    
    return render(request,'login/index.html')

def register(request):
    if request.method=="POST":
        user = User.objects.register(request.POST)
        if isinstance(user, list):
            for error in user:
                messages.add_message(request, messages.INFO, error, extra_tags="register")
            return redirect('/')
        else:
            request.session['name'] = user.first_name
            request.session['user_id'] = user.id
            return redirect('/quotation')
    return redirect('/')

def login(request):
    if request.method=="POST":
        user = User.objects.login(request.POST)
        if isinstance(user, list):
            for error in user:
                messages.add_message(request, messages.INFO, error, extra_tags="login")
            return redirect('/')
        else:
            request.session['name'] = user.first_name
            request.session['user_id'] = user.id
            return redirect('/quotation')
    return redirect('/')

def logout(request):
    request.session.clear()
    return redirect('/')
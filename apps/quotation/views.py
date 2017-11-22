# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect
from .models import User, Quotation
from django.contrib import messages
import datetime

# Create your views here.
def index(request):
    if 'user_id' not in request.session:
        return redirect('/')
    else:        
        context = { 'quotes': Quotation.objects.getUnfavoritedQuotes(request.session['user_id']),
                    'user': User.objects.get(id=request.session['user_id']),
                    'favs': Quotation.objects.getAllFav(request.session['user_id']) }
        return render(request,'quotation/index.html', context)

def addToList(request):
    if request.method == "POST":
        quote = Quotation.objects.validateQuote(request.POST)     
        if quote:
            for error in quote:
                messages.add_message(request, messages.INFO, error)
            return redirect('/quotation')
        else:
            postData = { 'user': request.session['user_id'],
                        'quotation': request.POST['quotation'],
                        'quoter': request.POST['quoter'] }
            quotation = Quotation.objects.addQuote(postData)
            if not isinstance(quotation, Quotation):
                messages.add_message(request, messages.ERROR, quotation)        
                return redirect('quotation/addToList') 
            return redirect('/quotation')

def addToMyList(request, id):        
    try:
        if request.method == "POST":            
            # add to favorite
            Quotation.objects.addFav(request.session['user_id'], id)
            return redirect('/quotation')
    except:
        print 'Cannot add to list'
        return redirect('/quotation')

def deleteList(request, id):
    try:
        if request.method == "POST":
            Quotation.objects.deleteFav(request.session['user_id'], id)
            return redirect('/quotation')
    except:
        print 'Cannot remove from fav list'
        return redirect('/quotation')   

def viewUser(request, user_id):
    if 'user_id' not in request.session:
        return redirect('/')
    else:
        context = { 'user': User.objects.get(id=user_id),
                    'quotes': Quotation.objects.getQuote(user_id),
                    'count': Quotation.objects.getQuote(user_id).count() }
        return render(request, 'quotation/user.html', context)
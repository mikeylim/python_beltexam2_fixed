# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect
from .models import User, Quotation, Favorite
from django.contrib import messages
import datetime

# Create your views here.
def index(request):
            # 'quotes' : Quotation.objects.getQuote(request.session['user_id']
    context = { 'quotes': Quotation.objects.getAllQuote(),
                'user': User.objects.get(id=request.session['user_id']),
                'favs': Favorite.objects.getAllFav() }
    return render(request,'quotation/index.html', context)

def addToList(request):
    if request.method == "POST":
        postData = { 'user': request.session['user_id'],
                     'quotation': request.POST['quotation'],
                     'quoter': request.POST['quoter'] }
        quotation = Quotation.objects.addQuote(postData)
        quote = Quotation.objects.quote(request.POST)
        if isinstance(quote, list):
            for error in quote:
                messages.add_message(request, messages.INFO, error)
        if not isinstance(quotation, Quotation):
            messages.add_message(request, messages.ERROR, quotation)        
            return redirect('quotation/addToList') 
        return redirect('/quotation')
    elif request.method == "GET":        
        context = { 'quotation': Quotation.objects.all() } 
        return render(request, 'quotation/add.html', context)   

def addToMyList(request, id):    
    try:
        if request.method == "GET":
            context = { 'quotation': Quotation.objects.get(id=id) }            
        elif request.method == "POST":
            context = { 'quotation': Quotation.objects.get(id=id) }
            # add to favorite before deleting
            postData = { 'user': request.session['user_id'],
                        'quote_id' : id,
                        'quotation': context['quotation'].quotation,
                        'quoter': context['quotation'].quoter }
            Favorite.objects.addFav(postData)
            # delete from Quotation
            Quotation.objects.get(id=id).delete()
            return redirect('/quotation', context)
    except:
        print 'Cannot delete this list'



def deleteList(request, id):
    try:
        if request.method == "GET":
            context = { 'favorite': Favorite.objects.get(id=id) }
            if request.session['user_id'] != context['favorite'].user.id:
                print 'Cannot delete this list'
            else:
                return render(request, 'quotation/delete.html', context)
        elif request.method == "POST":
            context = { 'favorite': Favorite.objects.get(id=id) }
            # add to quotation before deleting
            postData = { 'user': context['favorite'].user,
                         'quotation': context['favorite'].quotation,
                         'quoter': context['favorite'].quoter }
            Quotation.objects.addQuote(postData)
            # delete from Favorite
            Favorite.objects.get(id=id).delete()

            return redirect('/quotation', context)
    except:
        print 'Cannot delete this list'


    return redirect('/quotation')

def viewUser(request, user_id):
    context = { 'user': User.objects.get(id=user_id),
                'quotes': Quotation.objects.getQuote(user_id),
                'count': Quotation.objects.getQuote(user_id).count() }
    return render(request, 'quotation/user.html', context)
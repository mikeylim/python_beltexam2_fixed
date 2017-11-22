# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from ..login.models import User
import datetime

# Create your models here.
class QuoteManager(models.Manager):
    def addQuote(self, postData):
        user = User.objects.get(id=postData['user'])
        try:
            existing_quote = Quotation.objects.get(quotation=postData['quotation'])
            error = "The same quotation already exists!"
            return error
        except:            
            return Quotation.objects.create(quotation=postData['quotation'], user=user, quoter=postData['quoter'])

    def getUnfavoritedQuotes(self, user_id):
        unfav_quotes = []
        quotes = Quotation.objects.all().order_by('-id')
        for quote in quotes:
            if len(quote.favorited_by.filter(id=user_id)) == 0:
                unfav_quotes.append(quote)
        return unfav_quotes

    def getQuote(self, user_id):
        return Quotation.objects.filter(user=User.objects.get(id=user_id))

    def getAllQuote(self):
        return Quotation.objects.all()

    def getAllFav(self, user_id):        
        return Quotation.objects.filter(favorited_by=User.objects.get(id=user_id))    
    # return User.objects.get(id=user_id).favorites.all()
    
    def validateQuote(self, postData):
        errorMessages = []
        if len(postData['quoter']) < 3:
            errorMessages.append('Quoter has to be more than 3 characters')
        if len(postData['quotation']) < 10:
            errorMessages.append('Message has to be more than 10 characters')
        return errorMessages

    def addFav(self, user_id, quote_id):
        this_user = User.objects.get(id=user_id)
        this_quote = Quotation.objects.get(id=quote_id)
        errors = []

        if len(User.objects.filter(id=user_id)) == 0:
            errors.append('This is not a user')
        try:
            existing_quote = Quotation.objects.get(user=this_user)
            error = "The same favorite quotation already exists!"
            return error
        except:
            return this_user.favorites.add(this_quote)
    
    def deleteFav(self, user_id, quote_id):
        this_user = User.objects.get(id=user_id)
        this_quote = this_user.favorites.all().get(id=quote_id)
        errors = []

        if len(User.objects.filter(id=user_id)) == 0:
            errors.append('This is not a user')
        try:
            existing_quote = Quotation.objects.get(user=this_user)
            error = "The same favorite quotation already exists!"
            return error
        except:
            return this_user.favorites.remove(this_quote)



        # this_user = User.objects.get(id=user_id)
        # this_quote = this_user.favorites.all().get(id=quote_id)
        # # this_quote = this_user.favorites.get(id=quote_id)
        # # errors = []
        # # if len(User.objects.filter(id=user_id)) == 0:
        # #     errors.append('This is not a user')
        # # try:
        # #     existing_quote = Quotation.objects.get(user=this_user)
        # #     error = "The same favorite quotation already exists!"
        # #     return error
        # # except:
        # #     print 'in the except'
        # return this_user.favorites.remove(this_quote)

class Quotation(models.Model):
    quotation = models.CharField(max_length=255)
    quoter = models.CharField(max_length=55)
    user = models.ForeignKey(User, related_name="uploaded_quote")
    favorited_by = models.ManyToManyField(User, related_name="favorites")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = QuoteManager()
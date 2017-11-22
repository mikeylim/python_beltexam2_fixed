# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from ..login.models import User
import datetime

# Create your models here.
class QuoteManager(models.Manager):
    # def sortByCreatedAt(self):
    #     return 
    def addQuote(self, postData):
        user = User.objects.get(id=postData['user'])
        try:
            existing_quote = Quotation.objects.get(quotation=postData['quotation'])
            error = "The same quotation already exists!"
            return error
        except:            
            return Quotation.objects.create(quotation=postData['quotation'], user=user, quoter=postData['quoter'])

    def getQuote(self, user_id):
        return Quotation.objects.filter(user=User.objects.get(id=user_id))

    def getAllQuote(self):
        return Quotation.objects.all()
    # def getAllFav(self, id):
    #     q = Quotation.objects.get(id=id)
    #     return q.favorited_by.all()

class FavoriteManager(models.Manager):
    def getAllFav(self):
        return Favorite.objects.all()

    def getFav(self, user_id):
        return Favorite.objects.filter(user=User.objects.get(id=user_id))

    def addFav(self, postData):
        quote = Quotation.objects.get(id=postData['quote_id'])
        user = User.objects.get(id=postData['user'])
        try:
            existing_quote = Quotation.objects.get(quotation=postData['quotation'])
            error = "The same favorite quotation already exists!"
            return error
        except:            
            return Favorite.objects.create(favorites=quote, quotation=postData['quotation'], quoter=postData['quoter'], user=user)

class ValidateManager(models.Manager):
    def quote(self, postData):
        errorMessages = []
        if len(postData['quoter'] < 3):
            errorMessages.append('Quoter has to be more than 3 characters')
        if len(postData['message'] < 10):
            errorMessages.append('Message has to be more than 10 characters')
        return errorMessages
        

class Quotation(models.Model):
    quotation = models.CharField(max_length=255)
    quoter = models.CharField(max_length=55)
    user = models.ForeignKey(User, related_name="uploaded_quote")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = QuoteManager()

class Favorite(models.Model):
    quotation = models.CharField(max_length=255)
    quoter = models.CharField(max_length=55)
    favorites = models.ManyToManyField(User, related_name="favorited_by")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = FavoriteManager()
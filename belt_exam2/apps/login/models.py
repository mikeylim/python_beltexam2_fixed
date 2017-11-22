# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import re, bcrypt
from django.db import models
from datetime import datetime   
EMAIL_REGEX = re.compile(r'^[A-Za-z\d+-._]+@[A-Za-z\d+-._]+.[A-Za-z]+$')

# Create your models here.
class ValidateManager(models.Manager):
    def register(self, postData):
        errorMessages = []
        if len(postData["first_name"]) < 1 or len(postData['last_name']) < 1 or len(postData['password']) < 1 or len(postData['confirm']) < 1 or len(postData['email']) < 1 or len(postData['birthdate']) < 1 :
            errorMessages.append("All fields must not be blank")  
        else:                
            if postData["first_name"].isdigit():
                errorMessages.append("First cannot contain any numbers")

            if postData['last_name'].isdigit():
                errorMessages.append('Last name cannot contain any numbers')

            if postData['password'] != postData['confirm']:
                errorMessages.append('Password and Password Confirmation do not match')

            if len(postData['password']) < 8:
                errorMessages.append('Password must be at least 8 characters long')
            
            if not EMAIL_REGEX.match(postData['email']):
                errorMessages.append('Invalid email address')

            try:
                y, m, d = map(int, postData['birthdate'].split('-'))
                birthdate = datetime(y, m, d)
                if birthdate > datetime.now():
                    errorMessages.append('Birthdate must be before today')
            except:
                errorMessages.append('Please enter birthday field')

            if len(errorMessages) == 0:
                hashpw = bcrypt.hashpw(postData['password'].encode(), bcrypt.gensalt())
                newUser = User.objects.create(first_name=postData['first_name'], last_name=postData['last_name'], email=postData['email'], password=hashpw, birthdate=birthdate)
                return newUser       
        return errorMessages

    def login(self, postData):
        errorMessages = []
        try:
            user = User.objects.get(email=postData['email'])
            if bcrypt.hashpw(postData['password'].encode(), user.password.encode()) == user.password.encode():
                return user
            else:
                errorMessages.append('Invalid password')
                return errorMessages
        except:
            errorMessages.append('No user registered with that email')
            return errorMessages
class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    email = models.EmailField(max_length=255)
    birthdate = models.DateField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = ValidateManager()
    def __str__(self):
        return self.first_name + " " + self.last_name
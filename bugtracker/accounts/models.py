from django.conf import settings
from django.urls import reverse
from django.db import models
from django.contrib.auth import get_user_model
from django import template
from projects.models import *
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User,null=True,on_delete=models.CASCADE)
    profile_pic = models.ImageField(null=True,blank=True)
    first_name = models.CharField(max_length = 30,null=True)
    last_name = models.CharField(max_length = 30,null=True)
    phone = models.CharField(max_length = 14,null=True)
    occupation = models.CharField(max_length = 30,null=True)
    works_at = models.CharField(max_length = 30,null=True)
    skills = models.ManyToManyField(Tag) 
    country = models.CharField(max_length = 30,null=True)
    location = models.TextField()

    def __str__(self):
        return self.first_name
from django.conf import settings
from django.urls import reverse
from django.db import models
from django.contrib.auth import get_user_model
from django import template
from projects.models import *
from django.contrib.auth.models import User
from taggit.managers import TaggableManager


class Profile(models.Model):
    user = models.OneToOneField(User,null=True,on_delete=models.CASCADE)
    profile_pic = models.ImageField(null=True,blank=True,default = 'blank-profile-picture.jpg',upload_to='')
    first_name = models.CharField(max_length = 30,null=True)
    last_name = models.CharField(max_length = 30,null=True)
    phone = models.CharField(max_length = 14,null=True)
    occupation = models.CharField(max_length = 30,null=True)
    works_at = models.CharField(max_length = 30,null=True)
    skills = TaggableManager() 
    country = models.CharField(max_length = 30,null=True)
    location = models.TextField()
    reputation_points = models.IntegerField(default=0)
    online = models.BooleanField(default=False)

    def __str__(self):
        return str(self.first_name)
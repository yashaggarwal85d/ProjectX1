from django.db import models
from django.urls import reverse
from django.conf import settings
import misaka
from projects.models import *
from django.contrib.auth import get_user_model
# Create your models here.

User=get_user_model()

class Issue(models.Model):
    user = models.ForeignKey(User,on_delete=models.DO_NOTHING,related_name='issues')
    created_at = models.DateTimeField(auto_now=True)
    message = models.TextField()
    project = models.ForeignKey(Project,on_delete=models.DO_NOTHING,related_name="issues",null=True,blank=True)
    tags = models.ManyToManyField(Tags)

    def __str__(self):
        return self.message
    
    def save(self,*args,**kwargs):
        self.message_html=misaka.html(self.message)
        super().save(*args,**kwargs)
    
    def get_absolute_url(self):
        return reverse('issues:single',kwargs={'username':self.user.username,'pk':self.pk})

    class Meta:
        ordering = ['created_at']
        unique_together = ['user','message']
    
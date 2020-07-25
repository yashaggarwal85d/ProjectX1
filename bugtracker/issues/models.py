from django.db import models
from django.urls import reverse
from django.conf import settings
from projects.models import *
from django.contrib.auth import get_user_model
# Create your models here.

User=get_user_model()

class Issue(models.Model):

    name = models.CharField(max_length=255, unique=True)
    user = models.ForeignKey(User,null=True,on_delete=models.CASCADE,related_name='issues')
    created_at = models.DateTimeField(auto_now=True)
    message = models.TextField()
    project = models.ForeignKey(Project,on_delete=models.SET_NULL,related_name="issues",null=True,blank=True)
    tags = models.ManyToManyField(Tag)
    solve = models.BooleanField(default = False)
    members = models.ManyToManyField(User,through="IssueMember")

    def __str__(self):
        return self.name
    
    def save(self,*args,**kwargs):
        super().save(*args,**kwargs)
    
    def get_absolute_url(self):
        return reverse('issues:single',kwargs={'username':self.user.username,'pk':self.pk})

    class Meta:
        ordering = ['created_at']
        unique_together = ['user','name']
    
class IssueMember(models.Model):
    issue = models.ForeignKey(Issue,null=True,on_delete=models.CASCADE, related_name="memberships",)
    user = models.ForeignKey(User,null=True,on_delete=models.CASCADE ,related_name='user_issues',)

    def __str__(self):
        return self.user.username

    class Meta:
        unique_together = ("issue", "user")

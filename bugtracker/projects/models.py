from django.conf import settings
from django.urls import reverse
from django.db import models
from django.contrib.auth import get_user_model
from django import template
from taggit.managers import TaggableManager
from ckeditor.fields import RichTextField

User = get_user_model()
register = template.Library()

class Project(models.Model):
    user = models.ForeignKey(User,null=True,on_delete=models.CASCADE,related_name='projects')
    name = models.CharField(max_length=255, unique=True)
    created_at = models.DateTimeField(auto_now=True)
    description = RichTextField(blank=True,null=True)
    tags = TaggableManager()
    complete = models.BooleanField(default = False)
    members = models.ManyToManyField(User,through="ProjectMember")

    def __str__(self):
        return '%s - %s' % (self.name,self.user.username)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("projects:single", kwargs={"pk": self.pk})


    class Meta:
        ordering = ["name"]
        unique_together = ['user','name']

class ProjectMember(models.Model):
    project = models.ForeignKey(Project,null=True,on_delete=models.CASCADE, related_name="memberships",)
    user = models.ForeignKey(User,null=True,on_delete=models.CASCADE ,related_name='user_projects',)

    def __str__(self):
        return self.user.username

    class Meta:
        unique_together = ("project", "user")

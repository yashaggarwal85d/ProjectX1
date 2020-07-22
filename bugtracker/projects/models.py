from django.conf import settings
from django.urls import reverse
from django.db import models
from django.utils.text import slugify
import misaka
from django.contrib.auth import get_user_model
from django import template


User = get_user_model()
register = template.Library()

class Tag(models.Model):
    name = models.CharField(max_length=255, unique=True)
    def __str__(self):
        return self.name
    class Meta:
        ordering = ["name"]

class Project(models.Model):
    name = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(allow_unicode=True, unique=True)
    description = models.TextField(blank=True, default='')
    tags = models.ManyToManyField(Tag)
    members = models.ManyToManyField(User,through="ProjectMember")

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        self.description_html = misaka.html(self.description)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("projects:single", kwargs={"slug": self.slug})


    class Meta:
        ordering = ["name"]


class ProjectMember(models.Model):
    project = models.ForeignKey(Project,on_delete=models.DO_NOTHING, related_name="memberships",)
    user = models.ForeignKey(User,on_delete=models.DO_NOTHING ,related_name='user_projects',)

    def __str__(self):
        return self.user.username

    class Meta:
        unique_together = ("project", "user")

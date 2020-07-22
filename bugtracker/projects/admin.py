from django.contrib import admin

from . import models


class ProjectMemberInline(admin.TabularInline):
    model = models.ProjectMember



admin.site.register(models.Project)
admin.site.register(models.Tag)
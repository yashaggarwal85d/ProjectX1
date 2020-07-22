from django.contrib import admin
from . import models


class IssueMemberInline(admin.TabularInline):
    model = models.IssueMember



admin.site.register(models.Issue)
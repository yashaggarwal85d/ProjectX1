from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.urls import reverse
from django.db import IntegrityError
from django.shortcuts import get_object_or_404
from django.views import generic
from projects.models import Project,ProjectMember
from . import models

# Create your views here.

class CreateProject(LoginRequiredMixin,generic.CreateView):
    fields = ('name','description','tags')
    model = Project

class SingleProject(generic.DetailView):
    model = Project

class ListProjects(generic.ListView):
    model = Project

class JoinProject(LoginRequiredMixin, generic.RedirectView):

    def get_redirect_url(self, *args, **kwargs):
        return reverse("projects:single",kwargs={"slug": self.kwargs.get("slug")})

    def get(self, request, *args, **kwargs):
        project = get_object_or_404(Project,slug=self.kwargs.get("slug"))

        try:
            ProjectMember.objects.create(user=self.request.user,project=project)

        except IntegrityError:
            messages.warning(self.request,("Warning, already a member of {}".format(project.name)))

        else:
            messages.success(self.request,"You are now a member of the {} project.".format(project.name))

        return super().get(request, *args, **kwargs)


class LeaveProject(LoginRequiredMixin, generic.RedirectView):

    def get_redirect_url(self, *args, **kwargs):
        return reverse("projects:single",kwargs={"slug": self.kwargs.get("slug")})

    def get(self, request, *args, **kwargs):

        try:

            membership = models.ProjectMember.objects.filter(
                user=self.request.user,
                project__slug=self.kwargs.get("slug")
            ).get()

        except models.ProjectMember.DoesNotExist:
            messages.warning(
                self.request,
                "You can't leave this project because you aren't in it."
            )
        else:
            membership.delete()
            messages.success(
                self.request,
                "You have successfully left this project."
            )
        return super().get(request, *args, **kwargs)

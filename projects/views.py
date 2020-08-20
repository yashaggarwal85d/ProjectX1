from django.contrib import messages
from braces.views import SelectRelatedMixin
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.urls import reverse,reverse_lazy
from django.db import IntegrityError
from django.shortcuts import get_object_or_404,redirect,render
from django.views import generic
from projects.models import Project,ProjectMember
from issues.models import *
from . import models
from . import forms
from taggit.models import Tag
from django.contrib.auth.decorators import login_required
from rest_framework.views import APIView
from rest_framework import authentication, permissions
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import *

# Create your views here.

class CreateProject(LoginRequiredMixin, SelectRelatedMixin,generic.CreateView):
    
    model = Project
    form_class = forms.ProjectForm
    template_name = 'projects/project_form.html'
    
    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        form.save_m2m()
        return super().form_valid(form)

@login_required
def tagged(request,pk):
    tag=get_object_or_404(Tag,pk=pk)
    issues=Issue.objects.filter(tags=tag)
    projects=Project.objects.filter(tags=tag)
    search_term = str(tag)
    context = {'search_term':search_term,'tag':tag,'projects':projects,'issues':issues}
    return render(request,'search_result.html',context) 

class SingleProject(generic.DetailView):
    model = Project


@login_required
def ListProjects(request):
    projects = Project.objects.all()
    context = {'projects':projects}
    return render(request,'projects/project_list.html',context)


class JoinProject(LoginRequiredMixin, generic.RedirectView):

    def get_redirect_url(self, *args, **kwargs):
        return reverse("projects:single",kwargs={"pk": self.kwargs.get("pk")})

    def get(self, request, *args, **kwargs):
        project = get_object_or_404(Project,pk=self.kwargs.get("pk"))

        try:
            ProjectMember.objects.create(user=self.request.user,project=project)

        except IntegrityError:
            messages.warning(self.request,("Warning, already a member of {}".format(project.name)))

        else:
            messages.success(self.request,"You are now a member of the {} project.".format(project.name))

        return super().get(request, *args, **kwargs)


class LeaveProject(LoginRequiredMixin, generic.RedirectView):

    def get_redirect_url(self, *args, **kwargs):
        return reverse("projects:single",kwargs={"pk": self.kwargs.get("pk")})

    def get(self, request, *args, **kwargs):

        try:

            membership = models.ProjectMember.objects.filter(
                user=self.request.user,
                project__pk=self.kwargs.get("pk")
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



class DeleteProject(LoginRequiredMixin, SelectRelatedMixin,generic.DeleteView):
    model = models.Project
    select_related = ("user",)
    success_url = reverse_lazy("projects:all")

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(user_id=self.request.user.id)

    def delete(self, *args, **kwargs):
        messages.success(self.request, "Project Deleted")
        return super().delete(*args, **kwargs)

def CompleteProject(request,pk):

    project = models.Project.objects.get(id=pk)
    project.complete = True
    project.save()
    return redirect('projects:all')


#API

@login_required
@api_view(['GET'])
def projects_list_api(request):
    projects = models.Project.objects.all().order_by('id')
    serializer = ProjectSerializer(projects, many=True)
    return Response(serializer.data)

def CloseOrOpenJoin(request,pk):
    project = models.Project.objects.get(id=pk)
    if project.projectJoinPermission == True:
        project.projectJoinPermission = False
    else:
        project.projectJoinPermission = True
    project.save()
    return redirect('projects:single',pk)
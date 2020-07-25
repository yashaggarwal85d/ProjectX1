from django.http import  HttpResponse, Http404
from braces.views import SelectRelatedMixin
from . import forms
from . import models
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.urls import reverse,reverse_lazy
from django.db import IntegrityError
from django.shortcuts import get_object_or_404,render,redirect
from django.views import generic
from projects.models import Project,ProjectMember
from django.contrib.auth import get_user_model

User = get_user_model()

class IssueList(SelectRelatedMixin, generic.ListView):
    model = models.Issue
    select_related = ("user", "project")


class UserIssues(generic.ListView):
    model = models.Issue
    template_name = "issues/user_issue_list.html"

    def get_queryset(self):
        try:
            self.issue_user = User.objects.prefetch_related("issues").get(
                username__iexact=self.kwargs.get("username")
            )
        except User.DoesNotExist:
            raise Http404
        else:
            return self.issue_user.issues.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["issue_user"] = self.issue_user
        return context


class IssueDetail(SelectRelatedMixin, generic.DetailView):
    model = models.Issue
    select_related = ("user", "project")

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(
            user__username__iexact=self.kwargs.get("username")
        )

class CreateIssue(LoginRequiredMixin, SelectRelatedMixin, generic.CreateView):
    # form_class = forms.IssueForm
    fields = ('name','message','project','tags')
    model = models.Issue
    

    # def get_form_kwargs(self):
    #     kwargs = super().get_form_kwargs()
    #     kwargs.update({"user": self.request.user})
    #     return kwargs

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        return super().form_valid(form)


class DeleteIssue(LoginRequiredMixin, SelectRelatedMixin,generic.DeleteView):
    model = models.Issue
    select_related = ("user", "project")
    success_url = reverse_lazy("issues:all")

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(user_id=self.request.user.id)

    def delete(self, *args, **kwargs):
        messages.success(self.request, "Issue Deleted")
        return super().delete(*args, **kwargs)



class JoinIssue(LoginRequiredMixin, generic.RedirectView):

    def get_redirect_url(self, *args, **kwargs):
        return reverse("issues:all")

    def get(self, request, *args, **kwargs):
        issue = get_object_or_404(models.Issue,pk=self.kwargs.get("pk"))

        try:
            models.IssueMember.objects.create(user=self.request.user,issue=issue)

        except IntegrityError:
            messages.warning(self.request,("Warning, already a member of {}".format(issue.message)))

        else:
            messages.success(self.request,"You are now a member of the {} issue.".format(issue.message))

        return super().get(request, *args, **kwargs)


class LeaveIssue(LoginRequiredMixin, generic.RedirectView):

    def get_redirect_url(self, *args, **kwargs):
        return reverse("issues:all")

    def get(self, request, *args, **kwargs):

        try:

            membership = models.IssueMember.objects.filter(
                user=self.request.user,
                issue__pk=self.kwargs.get("pk")
            ).get()

        except models.IssueMember.DoesNotExist:
            messages.warning(
                self.request,
                "You can't leave this issue because you aren't in it."
            )
        else:
            membership.delete()
            messages.success(
                self.request,
                "You have successfully left this issue."
            )
        return super().get(request, *args, **kwargs)

def SolveIssue(request,pk):

    issue = models.Issue.objects.get(id=pk)
    issue.solve = True
    issue.save()
    return redirect('issues:all')

def UpdateIssue(request,pk):

    issue = models.Issue.objects.get(id=pk)
    form = forms.IssueForm(instance=issue)
    
    context = {'form':form}
    return render(request, 'issues/issue_form.html', context)
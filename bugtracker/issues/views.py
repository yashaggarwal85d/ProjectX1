from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin

from django.urls import reverse_lazy
from django.http import Http404
from django.views import generic

from braces.views import SelectRelatedMixin
from . import forms
from . import models

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
    fields = ('message','project','tags')
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


class DeleteIssue(LoginRequiredMixin, SelectRelatedMixin,):
    model = models.Issue
    select_related = ("user", "project")
    success_url = reverse_lazy("issues:all")

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(user_id=self.request.user.id)

    def delete(self, *args, **kwargs):
        messages.success(self.request, "Issue Deleted")
        return super().delete(*args, **kwargs)


from django import forms

from issues import models


class IssueForm(forms.ModelForm):
    class Meta:
        fields = ("message", "project","tags")
        model = models.Issue

    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)
        if user is not None:
            self.fields["project"].queryset = (
                models.Project.objects.filter(
                    pk__in=user.projects.values_list("project__pk")
                )
            )

            self.fields["tags"].queryset = (
                models.Tags.objects.filter(
                    pk__in=Tags.values_list("project__pk")
                )
            )

from django import forms
from issues import models
from projects.models import Project
from django.db.models import Q

class IssueForm(forms.ModelForm):
    class Meta:
        fields = '__all__'
        exclude = ['user','created_at','members']
        model = models.Issue
        labels = {'solve':'mark as solved ?'}
        help_texts = {'tags':''}

        widgets = {
            'name':forms.TextInput(attrs={'class':'form-control'}),
            'message':forms.Textarea(attrs={'class':'form-control'}),
            'project':forms.Select(attrs={'class':'form-control'}),
            'tags':forms.TextInput(attrs={'class':'form-control','data-role':'tagsinput','placeholder':'press enter to add more tags'}),
            'solve':forms.CheckboxInput(attrs={}),
            'deadline':forms.DateInput(attrs={'class':'form-control','type':'date'}),
            'priority':forms.Select(attrs={'class':'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)
        if user is not None:
            self.fields['project'].queryset = (
                models.Project.objects.filter( Q(user__pk=user.pk) | Q(members__pk=user.pk) )
            )




class AnswerForm(forms.ModelForm):
    class Meta:
        fields = ('message',)
        model=models.Answer
        labels = {'message':''}
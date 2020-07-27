from django import forms
from projects import models

class ProjectForm(forms.ModelForm):
    class Meta:
        fields = '__all__'
        exclude = ['user','created_at','members','complete']
        model = models.Project
        help_texts = {'tags':''}

        widgets = {
            'name':forms.TextInput(attrs={'class':'form-control'}),
            'description':forms.Textarea(attrs={'class':'form-control'}),
            'tags':forms.TextInput(attrs={'class':'form-control','data-role':'tagsinput','placeholder':'press enter to add more tags'}),
        } 
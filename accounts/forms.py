from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from .models import Profile
from taggit.forms import TagWidget

class CreateUserForm(UserCreationForm):
	class Meta:
		model = User
		fields = ['username', 'email', 'password1', 'password2']

class CreateProfileForm(ModelForm):
    class Meta:
        model = Profile
        fields = '__all__'
        exclude = ['user','reputation_points','online']
        help_texts = {'skills':''}
        labels = {'skills':'skills'}
        
        widgets = {
            'first_name':forms.TextInput(attrs={'class':'form-control'}),
            'last_name':forms.TextInput(attrs={'class':'form-control'}),
            'phone':forms.NumberInput(attrs={'class':'form-control'}),
            'occupation':forms.TextInput(attrs={'class':'form-control'}),
            'works_at':forms.TextInput(attrs={'class':'form-control'}),
            'country':forms.TextInput(attrs={'class':'form-control'}),
            'location':forms.TextInput(attrs={'class':'form-control'}),
            'linkedin':forms.URLInput(attrs={'class':'form-control'}),
            'twitter':forms.URLInput(attrs={'class':'form-control'}),
            'github':forms.URLInput(attrs={'class':'form-control'}),
            'skills':TagWidget(attrs={'class':'form-control','data-role':'tagsinput','placeholder':'press enter to add more skills'}),
        }

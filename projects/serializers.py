from rest_framework import serializers
from .models import Project

class ProjectSerializer(serializers.ModelSerializer):
	class Meta:
		model = Project
		fields = '__all__'

class ProjectRepoSerializer(serializers.ModelSerializer):
	class Meta:
		model = Project
		fields = ('repoowner','githubrepo',)
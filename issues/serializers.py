from rest_framework import serializers
from .models import Answer,Issue

class AnswerSerializer(serializers.ModelSerializer):
	class Meta:
		model = Answer
		fields ='__all__'

class IssueSerializer(serializers.ModelSerializer):
	class Meta:
		model = Issue
		fields = '__all__'
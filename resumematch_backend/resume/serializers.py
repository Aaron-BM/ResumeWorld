from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Resume


class ResumeSerializer(serializers.ModelSerializer):

  class Meta:
    model = Resume
    fields = ['id', 'upload', 'uploaded_at', 'parsed_text', 'email', 'skills' ]
    read_only_fields = [ 'uploaded_at', 'parsed_text', 'email', 'skills' ]


class UserRegistrationSerializer(serializers.ModelSerializer):
  password = serializers.CharField(write_only = True)
  
  class Meta:
    model = User
    fields = ['username', 'email', 'password']

  def create(self, validated_data):
    return User.objects.create_user(
      username=validated_data['username'],
      email=validated_data['email'],
      password=validated_data['password']
    )

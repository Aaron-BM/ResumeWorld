from django.db import models
from django.contrib.auth.models import User
from django.db.models import JSONField
from django.contrib.postgres.fields import ArrayField
# Create your models here.

class Resume(models.Model):
  user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='resumes')
  upload = models.FileField(upload_to='resumes/', max_length=100, blank=True,  null=True)
  uploaded_at = models.DateTimeField(auto_now_add=True)
  parsed_text = models.TextField(blank=True, null=True)
  email = models.CharField(max_length=50, blank=True, null=True)
  skills = models.JSONField( blank=True, null=True)


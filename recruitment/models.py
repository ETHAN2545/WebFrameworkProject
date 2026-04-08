from django.conf import settings
from django.db import models

class Skill(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class CandidateProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    bio = models.TextField(blank=True)
    experience = models.PositiveIntegerField(default=0, help_text="Years of experience")
    skills = models.ManyToManyField(Skill, blank=True)

    def __str__(self):
        return self.full_name
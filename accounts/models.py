from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    ADMIN = 'ADMIN'
    RECRUITER = 'RECRUITER'
    CANDIDATE = 'CANDIDATE'
    HIRING_MANAGER = 'HIRING_MANAGER'

    ROLE_CHOICES = [
        (ADMIN, 'Admin'),
        (RECRUITER, 'Recruiter'),
        (CANDIDATE, 'Candidate'),
        (HIRING_MANAGER, 'Hiring Manager'),
    ]

    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default=CANDIDATE)

    def __str__(self):
        return self.username
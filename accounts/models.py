from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    ADMIN = 'ADMIN'
    RECRUITER = 'RECRUITER'
    CANDIDATE = 'CANDIDATE'

    ROLE_CHOICES = [
        (ADMIN, 'Admin'),
        (RECRUITER, 'Recruiter'),
        (CANDIDATE, 'Candidate'),
    ]

    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default=CANDIDATE)

    def __str__(self):
        return self.username
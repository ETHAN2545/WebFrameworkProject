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
    
class Job(models.Model):
    recruiter = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        limit_choices_to={'role': 'RECRUITER'}
    )
    title = models.CharField(max_length=200)
    description = models.TextField()
    location = models.CharField(max_length=100)
    salary = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    required_skills = models.ManyToManyField(Skill, blank=True)
    
    def __str__(self):
        return self.title
    
class Application(models.Model):
    PENDING = 'PENDING'
    REVIEWED = 'REVIEWED'
    SHORTLISTED = 'SHORTLISTED'
    REJECTED = 'REJECTED'
    
    STATUS_CHOICES = [
        (PENDING, 'Pending'),
        (REVIEWED, 'Reviewed'),
        (SHORTLISTED, 'Shortlisted'),
        (REJECTED, 'Rejected'),
    ]
    
    candidate = models.ForeignKey(CandidateProfile, on_delete=models.CASCADE)
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    cover_letter = models.TextField(blank=True)
    applied_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=PENDING)
    
    class Meta:
        unique_together = ['candidate', 'job']
        
    def __str__(self):
        return f"{self.candidate.full_name} - {self.job.title}"
    
class Interview(models.Model):
    application = models.ForeignKey(Application, on_delete=models.CASCADE)
    interview_date = models.DateTimeField()
    location = models.CharField(max_length=200)
    notes = models.TextField(blank=True)
    
    def __str__(self):
        return f"Interview for {self.application.candidate.full_name} - {self.application.job.title}"
from django.contrib import admin
from .models import CandidateProfile, Skill, Job, Application

admin.site.register(CandidateProfile)
admin.site.register(Skill)
admin.site.register(Job)
admin.site.register(Application)
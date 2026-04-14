from django.contrib import admin
from .models import CandidateProfile, Skill, Job, Application, Interview

admin.site.register(CandidateProfile)
admin.site.register(Skill)
admin.site.register(Job)
admin.site.register(Application)
admin.site.register(Interview)
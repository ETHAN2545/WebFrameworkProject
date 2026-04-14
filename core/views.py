from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from recruitment.models import CandidateProfile, Job, Application, Interview

def home(request):
    return render(request, 'core/home.html')

@login_required
def dashboard(request):
    context = {}
    
    if request.user.role == 'CANDIDATE':
        profile = CandidateProfile.objects.filter(user=request.user).first()
        applications_count = 0
        interviews_count = 0
        
        if profile:
            applications_count = Application.objects.filter(candidate=profile).count()
            interviews_count = Interview.objects.filter(application__candidate=profile).count()
        
        context = {
            'profile': profile,
            'applications_count': applications_count,
            'interviews_count': interviews_count,
        }
    
    elif request.user.role == 'RECRUITER':
        jobs_count = Job.objects.filter(recruiter=request.user).count()
        applications_count = Application.objects.filter(job__recruiter=request.user).count()
        interviews_count = Interview.objects.filter(application__job__recruiter=request.user).count()
        
        context = {
            'jobs_count': jobs_count,
            'applications_count': applications_count,
            'interviews_count': interviews_count,
        }
        
    return render(request, 'core/dashboard.html', context)
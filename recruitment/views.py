from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.shortcuts import render, redirect, get_object_or_404

from .forms import CandidateProfileForm, SkillForm, JobForm, ApplicationForm, ApplicationStatusForm, InterviewForm
from .models import CandidateProfile, Skill, Job, Application, Interview

def candidate_required(user):
    return user.role == 'CANDIDATE'

def recruiter_required(user):
    return user.role == 'RECRUITER'

@login_required
def profile_view(request):
    if not candidate_required(request.user):
        return HttpResponseForbidden("Only candidates can access this page.")

    profile = CandidateProfile.objects.filter(user=request.user).first()
    return render(request, 'recruitment/profile.html', {'profile': profile})

@login_required
def create_profile(request):
    if not candidate_required(request.user):
        return HttpResponseForbidden("Only candidates can access this page.")

    if CandidateProfile.objects.filter(user=request.user).exists():
        return redirect('profile')

    if request.method == 'POST':
        form = CandidateProfileForm(request.POST)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = request.user
            profile.save()
            return redirect('profile')
    else:
        form = CandidateProfileForm()

    return render(request, 'recruitment/profile_form.html', {'form': form})

@login_required
def edit_profile(request):
    if not candidate_required(request.user):
        return HttpResponseForbidden("Only candidates can access this page.")

    profile = get_object_or_404(CandidateProfile, user=request.user)

    if request.method == 'POST':
        form = CandidateProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = CandidateProfileForm(instance=profile)

    return render(request, 'recruitment/profile_form.html', {'form': form})

@login_required
def add_skill(request):
    if not candidate_required(request.user):
        return HttpResponseForbidden("Only candidates can access this page.")

    profile = get_object_or_404(CandidateProfile, user=request.user)

    if request.method == 'POST':
        form = SkillForm(request.POST)
        if form.is_valid():
            skill_name = form.cleaned_data['name']
            skill, created = Skill.objects.get_or_create(name=skill_name)
            profile.skills.add(skill)
            return redirect('profile')
    else:
        form = SkillForm()

    return render(request, 'recruitment/add_skill.html', {'form': form})

@login_required
def remove_skill(request, skill_id):
    if not candidate_required(request.user):
        return HttpResponseForbidden("Only candidates can access this page.")

    profile = get_object_or_404(CandidateProfile, user=request.user)
    skill = get_object_or_404(Skill, id=skill_id)

    profile.skills.remove(skill)
    return redirect('profile')

@login_required
def job_list(request):
    jobs = Job.objects.all().order_by('-created_at')
    return render(request, 'recruitment/job_list.html', {'jobs': jobs})

@login_required
def job_detail(request, job_id):
    job = get_object_or_404(Job, id=job_id)
    already_applied = False
    
    if request.user.role == 'CANDIDATE':
        profile = CandidateProfile.objects.filter(user=request.user).first()
        if profile:
            already_applied = Application.objects.filter(candidate=profile, job=job).exists()
            
    return render(request, 'recruitment/job_detail.html', {
        'job': job,
        'already_applied': already_applied
    })
    
@login_required
def create_job(request):
    if not recruiter_required(request.user):
        return HttpResponseForbidden("Only recruiters can access this page!")
    
    if request.method == 'POST':
        form = JobForm(request.POST)
        if form.is_valid():
            job = form.save(commit=False)
            job.recruiter = request.user
            job.save()
            form.save_m2m()
            return redirect('job_list')
    else:
        form = JobForm()
        
    return render(request, 'recruitment/job_form.html', {'form': form, 'title': 'Create Job'})

@login_required
def edit_job(request, job_id):
    if not recruiter_required(request.user):
        return HttpResponseForbidden("Only recruiters can access this page!")
    
    job = get_object_or_404(Job, id=job_id, recruiter=request.user)
    
    if request.method == 'POST':
        form = JobForm(request.POST, instance=job)
        if form.is_valid():
            form.save()
            return redirect('job_detail', job_id=job_id)
        
    else:
        form = JobForm(instance=job)
        
    return render(request, 'recruitment/job_form.html', {'form': form, 'title': 'Edit Job'})

@login_required
def delete_job(request, job_id):
    if not recruiter_required(request.user):
        return HttpResponseForbidden("Only recruiters can access this page!")
    
    job = get_object_or_404(Job, id=job_id, recruiter=request.user)
    
    if request.method == 'POST':
        job.delete()
        return redirect('job_list')
    
    return render(request, 'recruitment/job_confirm_delete.html', {'job': job})

@login_required
def apply_for_job(request, job_id):
    if not candidate_required(request.user):
        return HttpResponseForbidden("Only candidates can apply for jobs.")

    job = get_object_or_404(Job, id=job_id)
    profile = get_object_or_404(CandidateProfile, user=request.user)

    if Application.objects.filter(candidate=profile, job=job).exists():
        return redirect('job_detail', job_id=job.id)

    if request.method == 'POST':
        form = ApplicationForm(request.POST)
        if form.is_valid():
            application = form.save(commit=False)
            application.candidate = profile
            application.job = job
            application.save()
            return redirect('my_applications')
    else:
        form = ApplicationForm()

    return render(request, 'recruitment/apply_for_job.html', {'form': form, 'job': job})


@login_required
def my_applications(request):
    if not candidate_required(request.user):
        return HttpResponseForbidden("Only candidates can access this page.")

    profile = get_object_or_404(CandidateProfile, user=request.user)
    applications = Application.objects.filter(candidate=profile).order_by('-applied_at')

    return render(request, 'recruitment/my_applications.html', {'applications': applications})

@login_required
def recruiter_applications(request):
    if not recruiter_required(request.user):
        return HttpResponseForbidden("Only recruiters can access this page.")
    
    applications = Application.objects.filter(job__recruiter=request.user).order_by('-applied_at')
    return render(request, 'recruitment/recruiter_applications.html', {'applications': applications})

@login_required
def update_application_status(request, application_id):
    if not recruiter_required(request.user):
        return HttpResponseForbidden("Only recruiters can access this page.")
    
    application = get_object_or_404(Application, id=application_id, job__recruiter=request.user)
    
    if request.method == 'POST':
        form = ApplicationStatusForm(request.POST, instance=application)
        if form.is_valid():
            form.save()
            return redirect('recruiter_applications')
    else:
        form = ApplicationStatusForm(instance=application)
        
    return render(request, 'recruitment/update_application_status.html', {
        'form': form,
        'application': application
    })
    
@login_required
def schedule_interview(request, application_id):
    if not recruiter_required(request.user):
        return HttpResponseForbidden("Only recruiters can access this page.")
    
    application = get_object_or_404(Application, id=application_id, job__recruiter=request.user)
    
    if request.method == 'POST':
        form = InterviewForm(request.POST)
        if form.is_valid():
            interview = form.save(commit=False)
            interview.application = application
            interview.save()
            return redirect('recruiter_applications')
    else:
        form = InterviewForm()

    return render(request, 'recruitment/schedule_interview.html', {
        'form': form,
        'application': application
    })


@login_required
def my_interviews(request):
    if not candidate_required(request.user):
        return HttpResponseForbidden("Only candidates can access this page.")

    profile = get_object_or_404(CandidateProfile, user=request.user)
    interviews = Interview.objects.filter(application__candidate=profile).order_by('interview_date')

    return render(request, 'recruitment/my_interviews.html', {'interviews': interviews})
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.shortcuts import render, redirect, get_object_or_404

from .forms import CandidateProfileForm, SkillForm
from .models import CandidateProfile, Skill

def candidate_required(user):
    return user.role == 'CANDIDATE'

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
from django import forms
from .models import CandidateProfile, Skill

class CandidateProfileForm(forms.ModelForm):
    class Meta:
        model = CandidateProfile
        fields = ['full_name', 'phone', 'bio', 'experience']

class SkillForm(forms.ModelForm):
    class Meta:
        model = Skill
        fields = ['name']
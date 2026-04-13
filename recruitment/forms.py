from django import forms
from .models import CandidateProfile, Skill, Job, Application

class CandidateProfileForm(forms.ModelForm):
    class Meta:
        model = CandidateProfile
        fields = ['full_name', 'phone', 'bio', 'experience']

class SkillForm(forms.ModelForm):
    class Meta:
        model = Skill
        fields = ['name']
        
class JobForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = ['title', 'description', 'location', 'salary', 'required_skills']
        widgets = {
            'required_skills': forms.CheckboxSelectMultiple,
        }
        
class ApplicationForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = ['cover_letter']
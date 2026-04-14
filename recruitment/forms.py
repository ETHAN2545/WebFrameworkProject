from django import forms
from .models import CandidateProfile, Skill, Job, Application, Interview

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
        
class ApplicationStatusForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = ['status']
        
class InterviewForm(forms.ModelForm):
    class Meta:
        model = Interview 
        fields = ['interview_date', 'location', 'notes']
        widgets = {
            'interview_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }
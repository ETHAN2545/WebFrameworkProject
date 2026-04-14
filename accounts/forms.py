from django.contrib.auth.forms import UserCreationForm
from .models import User

class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'role', 'password1', 'password2']
        
    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = 'CANDIDATE'
        if commit:
            user.save()
        return user
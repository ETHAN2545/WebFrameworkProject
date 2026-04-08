from django.urls import path
from . import views

urlpatterns = [
    path('profile/', views.profile_view, name='profile'),
    path('profile/create/', views.create_profile, name='create_profile'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    path('skills/add/', views.add_skill, name='add_skill'),
    path('skills/remove/<int:skill_id>/', views.remove_skill, name='remove_skill'),
]
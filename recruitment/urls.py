from django.urls import path
from . import views

urlpatterns = [
    path('profile/', views.profile_view, name='profile'),
    path('profile/create/', views.create_profile, name='create_profile'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    path('skills/add/', views.add_skill, name='add_skill'),
    path('skills/remove/<int:skill_id>/', views.remove_skill, name='remove_skill'),
    
    path('jobs/', views.job_list, name='job_list'),
    path('jobs/<int:job_id>/', views.job_detail, name='job_detail'),
    path('jobs/create/', views.create_job, name='create_job'),
    path('jobs/<int:job_id>/edit/', views.edit_job, name='edit_job'),
    path('jobs/<int:job_id>/delete/', views.delete_job, name='delete_job'),

    path('jobs/<int:job_id>/apply/', views.apply_for_job, name='apply_for_job'),
    path('applications/', views.my_applications, name='my_applications'),
    
    path('recruiter/applications/', views.recruiter_applications, name='recruiter_applications'),
    path('applications/<int:application_id>/status/', views.update_application_status, name='update_application_status'),
    path('applications/<int:application_id>/interview/', views.schedule_interview, name='schedule_interview'),

    path('interviews/', views.my_interviews, name='my_interviews'),
]
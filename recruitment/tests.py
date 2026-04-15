from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from .models import CandidateProfile, Skill, Job, Application

User = get_user_model()


class RecruitmentModelTests(TestCase):
    def setUp(self):
        self.candidate_user = User.objects.create_user(
            username='candidate1',
            password='Testpass123!',
            role='CANDIDATE'
        )
        self.recruiter_user = User.objects.create_user(
            username='recruiter1',
            password='Testpass123!',
            role='RECRUITER'
        )
        self.profile = CandidateProfile.objects.create(
            user=self.candidate_user,
            full_name='Candidate One',
            phone='123456789',
            bio='Finance graduate',
            experience=1
        )
        self.skill = Skill.objects.create(name='Excel')
        self.job = Job.objects.create(
            recruiter=self.recruiter_user,
            title='Junior Analyst',
            description='Finance role',
            location='Dublin',
            salary=30000
        )

    def test_skill_string(self):
        self.assertEqual(str(self.skill), 'Excel')

    def test_candidate_profile_string(self):
        self.assertEqual(str(self.profile), 'Candidate One')

    def test_job_string(self):
        self.assertEqual(str(self.job), 'Junior Analyst')


class RecruitmentViewTests(TestCase):
    def setUp(self):
        self.candidate_user = User.objects.create_user(
            username='candidate1',
            password='Testpass123!',
            role='CANDIDATE'
        )
        self.recruiter_user = User.objects.create_user(
            username='recruiter1',
            password='Testpass123!',
            role='RECRUITER'
        )
        self.profile = CandidateProfile.objects.create(
            user=self.candidate_user,
            full_name='Candidate One',
            phone='123456789',
            bio='Finance graduate',
            experience=1
        )
        self.job = Job.objects.create(
            recruiter=self.recruiter_user,
            title='Junior Analyst',
            description='Finance role',
            location='Dublin',
            salary=30000
        )

    def test_candidate_can_view_jobs(self):
        self.client.login(username='candidate1', password='Testpass123!')
        response = self.client.get(reverse('job_list'))
        self.assertEqual(response.status_code, 200)

    def test_candidate_can_apply_for_job(self):
        self.client.login(username='candidate1', password='Testpass123!')
        response = self.client.post(reverse('apply_for_job', args=[self.job.id]), {
            'cover_letter': 'I am interested in this job.'
        })
        self.assertEqual(Application.objects.count(), 1)

    def test_recruiter_can_create_job(self):
        self.client.login(username='recruiter1', password='Testpass123!')
        response = self.client.post(reverse('create_job'), {
            'title': 'Tax Assistant',
            'description': 'Tax support role',
            'location': 'Dublin',
            'salary': 32000,
            'required_skills': []
        })
        self.assertEqual(Job.objects.count(), 2)

    def test_recruiter_cannot_access_candidate_profile_page(self):
        self.client.login(username='recruiter1', password='Testpass123!')
        response = self.client.get(reverse('profile'))
        self.assertEqual(response.status_code, 403)
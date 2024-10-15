from django.test import TestCase
from django.contrib.auth.models import User
from .models import Activity

class ActivityModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.activity = Activity.objects.create(
            user=self.user, activity_type='Running', duration=30, distance=5.0, calories_burned=300, date='2024-10-05')

    def test_activity_creation(self):
        self.assertEqual(self.activity.user.username, 'testuser')
        self.assertEqual(self.activity.activity_type, 'Running')


from django.test import TestCase
from main.models import UserProfile


class UserModelTestCase(TestCase):

    def test_create_user(self):
        user, user_created = UserProfile.objects.create(username="John-Doe")
        self.assertEqual("John-Doe", user.slug)

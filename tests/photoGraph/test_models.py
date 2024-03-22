import json
from django.test import TestCase, RequestFactory
from django.urls import reverse
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from main.models import *
from django.core.files.uploadedfile import SimpleUploadedFile
from unittest.mock import patch

# run tests with command - python .\manage.py test tests.photoGraph.test_models
# all test cases pass as of 22/03/2024 14:30

class UserProfileModelTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass123')

    def test_user_profile_creation(self):
        profile = UserProfile.objects.create(user=self.user, biography="Test Bio")
        self.assertEqual(profile.slug, 'testuser')
        self.assertEqual(profile.biography, "Test Bio")

    def test_user_profile_creation_invalid(self):
        profile = UserProfile(user=self.user, biography='test bio' * 101)
        with self.assertRaises(ValidationError):
            profile.full_clean()  

class GroupModelTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='groupuser', password='grouppass123')
        self.user_profile = UserProfile.objects.create(user=self.user)

    def test_group_creation(self):
        group = Group.objects.create(created_by=self.user_profile, name="Test Group")
        group.save()
        self.assertIn(self.user_profile, group.members.all())
        self.assertEqual(group.slug, 'test-group')

class PostModelTestCase(TestCase):
    @patch('main.models.Post.save', autospec=True)
    def setUp(self, mock_save):
        user = User.objects.create_user(username='testuser', password='testpass123')
        user_profile = UserProfile.objects.create(user=user)
        self.group = Group.objects.create(created_by=user_profile, name="Test Group")
        self.post = Post.objects.create(
            created_by=user_profile,
            caption="Test Caption",
            photo="test_photo.jpg",
            latitude=55.00,
            longitude=-4.00,
            group=self.group
        )
        mock_save.assert_called_once()

    def test_post_creation(self):
        self.assertEqual(self.post.caption, "Test Caption")
        self.assertNotEqual(self.post.location_name, 'Unkown')
        self.assertEqual(self.post.latitude, 55.00)
        self.assertEqual(self.post.longitude, -4.00)

class CommentModelTestCase(TestCase):
    def setUp(self):
        user = User.objects.create_user(username='testuser', password='testpass123')
        self.user_profile = UserProfile.objects.create(user=user)
        self.group = Group.objects.create(created_by=self.user_profile, name="Test Group")
        self.post = Post.objects.create(
            created_by=self.user_profile,
            caption="Test Caption",
            photo="test_photo.jpg",
            latitude=55.00,
            longitude=-4.00,
            group=self.group
        )
    def test_comment_model_creation(self):
        self.create_comment = Comment.objects.create(created_by=self.user_profile, post = self.post, comment = 'blah')
        self.assertEqual(self.create_comment.comment, 'blah')

class PostReportModelTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='reporter', password='testpass123')
        self.reporter_profile = UserProfile.objects.create(user=self.user)
        self.post_owner = User.objects.create_user(username='postowner', password='postpass123')
        self.post_owner_profile = UserProfile.objects.create(user=self.post_owner)
        self.post = Post.objects.create(
            created_by=self.post_owner_profile,
            caption="Sample Post",
            photo="post_photo.jpg",
            latitude=0.0,
            longitude=0.0
        )

    def test_post_report_model_creation(self):
        report = PostReport.objects.create(
            reporter=self.reporter_profile,
            post_id=self.post,
            reason="Inappropriate content"
        )
        self.assertEqual(report.reporter, self.reporter_profile)
        self.assertEqual(report.post_id, self.post)
        self.assertEqual(report.reason, "Inappropriate content")
        self.assertIn("Report by", str(report))
    
class UserReportModelTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='reporter', password='testpass123')
        self.reporter_profile = UserProfile.objects.create(user=self.user)
        self.reported_user = User.objects.create_user(username='reporteduser', password='reportedpass123')

    def test_user_report_model_creation(self):
        report = UserReport.objects.create(
            reporter=self.reporter_profile,
            user_id=self.reported_user,
            reason="Spamming"
        )
        self.assertEqual(report.reporter, self.reporter_profile)
        self.assertEqual(report.user_id, self.reported_user)
        self.assertEqual(report.reason, "Spamming")
        
class LikeModelTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass123')
        self.user_profile = UserProfile.objects.create(user=self.user)
        self.post_creator_user = User.objects.create_user(username='postcreator', password='testpass123')
        self.post_creator_profile = UserProfile.objects.create(user=self.post_creator_user)
        self.post = Post.objects.create(
            created_by=self.post_creator_profile,
            caption="Sample Post",
            photo="post_photo.jpg",
            latitude=0.0,
            longitude=0.0
        )

    def test_like_model_creation(self):
        like = Like.objects.create(
            user=self.user_profile,
            post=self.post
        )

        self.assertEqual(like.user, self.user_profile)
        self.assertEqual(like.post, self.post)

        expected_str = f"{self.user_profile} likes {self.post.slug}"
        self.assertEqual(str(like), expected_str)

class ContactUsModelTestCase(TestCase):
    def setUp(self):
        self.contact_us = ContactUs.objects.create(
            name="name",
            email="name@example.com",
            subject="Test Subject",
            message="test message."
        )

    def test_contact_us_model_creation(self):
        self.assertEqual(self.contact_us.name, "name")
        self.assertEqual(self.contact_us.email, "name@example.com")
        self.assertEqual(self.contact_us.subject, "Test Subject")
        self.assertEqual(self.contact_us.message, "test message.")

    def test_contact_us_model_str(self):
        expected_str = "Message from name"
        self.assertEqual(str(self.contact_us), expected_str)

    def test_contact_us_get_details(self):
        expected_details = (
            "Name: name\n"
            "Email: name@example.com\n"
            "Subject: Test Subject\n"
            "Message: test message.\n"
        )
        self.assertEqual(self.contact_us.get_details(), expected_details)

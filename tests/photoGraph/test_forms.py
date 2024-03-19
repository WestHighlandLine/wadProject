from django.test import TestCase
from django.contrib.auth.models import User
from main.models import UserProfile, Group, Comment, Post, Report
from main.forms import (
    UserForm,
    UserProfileForm,
    GroupForm,
    PostForm,
    CommentForm,
    ReportForm,
)


class FormsTestCase(TestCase):

    def test_user_form_password_matching(self):
        form_data = {
            "username": "testuser",
            "email": "test@example.com",
            "password": "password123",
            "confirm_password": "password123",
        }
        form = UserForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_user_form_incorrect_password(self):
        form_data = {
            "username": "testuser",
            "email": "test@example.com",
            "password": "password123",
            "confirm_password": "password123",
        }
        form = UserForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_comment_form(self):
        import datetime

        user = User.objects.create(
            username="commenter", email="commenter@example.com", password="password123"
        )
        post = Post.objects.create(
            caption="test post", photo="test.jpg", latitude=0.0, longitude=0.0
        )
        form_data = {
            "commenter": user.pk,
            "post": post.pk,
            "comment": "test",
            "time": datetime.datetime.now(),
        }
        form = CommentForm(data=form_data)
        self.assertTrue(form.is_valid())

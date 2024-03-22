from django.test import TestCase, RequestFactory
from django.contrib.auth.models import User
from main.models import UserProfile, Group, Comment, Post, PostReport, UserReport
from main.forms import *

from django.core.files.uploadedfile import SimpleUploadedFile

# run tests with command python - .\manage.py test tests.photoGraph.test_forms
# all test cases pass as of 22/03/2024 14:30
class UserProfileTestCase(TestCase):
    def test_user_profile_form_valid(self):
        form_data = {
            'biography': 'This is a test bio',
        }
        with open('tests/photoGraph/test_images/test_image.jpg', 'rb') as image_file:
            file_data = {
                'profile_picture': SimpleUploadedFile('test_image.jpg', image_file.read(), content_type='image/jpeg'),
            }
        form = UserProfileForm(data=form_data, files=file_data)
        if not form.is_valid():
            self.fail(f"UserProfileForm is not valid: {form.errors.as_json()}")
        self.assertTrue(form.is_valid())

    def test_user_profile_form_invalid(self):
        form_data = {
            'biography': 'x' * 101,  
        }
        form = UserProfileForm(data=form_data)
        self.assertFalse(form.is_valid())

class UserFormTestCase(TestCase):
    def test_user_form_correct_password(self):
        form_data = {
            "username": "testuser",
            "email": "test@example.com",
            "password": "password123!",
            "confirm_password": "password123!",
        }
        form = UserForm(data=form_data)
        if not form.is_valid():
            self.fail(f"Form validation failed. Errors: {form.errors}")
        self.assertTrue(form.is_valid())

    def test_user_form_incorrect_password(self):
        form_data = {
            "username": "testuser",
            "email": "test@example.com",
            "password": "password123!",
            "confirm_password": "differentpassword123!",
        }
        form = UserForm(data=form_data)
        self.assertFalse(form.is_valid())

class CommentFormTestCase(TestCase):
    def test_comment_form(self):

        user = User.objects.create_user('testuser', 'test@example.com', 'testpassword123')

        with open('tests/photoGraph/test_images/test_image.jpg', 'rb') as image_file:
            user_profile = UserProfile.objects.create(
                user=user,
                biography='This is a test bio',
                profile_picture=SimpleUploadedFile('test_image.jpg', image_file.read(), content_type='image/jpeg')
            )

        post = Post.objects.create(
            caption="test post",
            photo="test.jpg",
            latitude=0.0,
            longitude=0.0,
            created_by=user_profile  
        )

        comment_form_data = {
            "post": post.pk,
            "comment": "test",
        }

        form = CommentForm(data=comment_form_data)
        self.assertTrue(form.is_valid())

class ContactUsFormTestCase(TestCase):
    def test_contact_us_form_valid(self):
        form_data = {
            'name': 'John Doe',
            'email': 'john@example.com',
            'subject': 'Test Subject',
            'message': 'This is a test message',
        }
        form = ContactUsForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_contact_us_form_invalid(self):
        form_data = {
            'name': 'John Doe',
            'email': 'not an email',
            'subject': 'Test Subject',
            'message': 'This is a test message',
        }
        form = ContactUsForm(data=form_data)
        self.assertFalse(form.is_valid())
    
class ReportFormTestCase(TestCase):
    def test_report_form_valid(self):
        form_data = {
            'reason': 'This is a test reason for reporting',
        }
        form = ReportForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_report_form_invalid(self):
        form_data = {
            'reason': '',
        }
        form = ReportForm(data=form_data)
        self.assertFalse(form.is_valid())


class PostFormTestCase(TestCase):
    def test_post_form_valid(self):
        user = User.objects.create_user('testuser2', 'test2@example.com', 'password1234!')
        user_profile = UserProfile.objects.create(user=user)

        request_factory = RequestFactory()
        request = request_factory.get('dummypath/to/view')
        request.user = user
        
        with open('tests/photoGraph/test_images/test_image.jpg', 'rb') as image_file:
            file_data = {
                'photo':SimpleUploadedFile('test_image.jpg', image_file.read(), content_type='image.jpeg')
            }
        form_data = {
            'caption':'Test',
            'latitude':0.0,
            'longitude':0.0,
        }
        form = PostForm(data=form_data, files=file_data, request = request)
        self.assertTrue(form.is_valid(), msg=form.errors)

    def test_post_form_invalid(self):

        user = User.objects.create_user('testuser2', 'test2@example.com', 'password1234!')
        user_profile = UserProfile.objects.create(user=user)

        request_factory = RequestFactory()
        request = request_factory.get('dummypath/to/view')
        request.user = user
        form_data = {
            'caption': 'Test Post',
            'latitude': '0.0',
            'longitude': '0.0',
        }
        form = PostForm(data=form_data, request = request)
        self.assertFalse(form.is_valid())

class ChangePostFormTestCase(TestCase):

    from unittest.mock import patch

    @patch('main.forms.ChangePost.clean')
    def test_change_post_form_valid(self, mock_clean):
        # Setup mock to return a specific cleaned_data
        mock_clean.return_value = {'caption': 'Valid Caption', 'photo': 'Valid Photo Path', 'latitude':'0.0',
                                   'longitude':'0.0'}
        
        with open('tests/photoGraph/test_images/test_image.jpg', 'rb') as img:
            file_data = {
                'photo':SimpleUploadedFile('test_image.jpg', img.read(), content_type='image.jpeg')
            }
        form_data = {
                'caption': 'Test Caption',
                'latitude': '0.0',
                'longitude': '0.0',
            }    
        form = ChangePost(data=form_data, files=file_data)
        self.assertTrue(form.is_valid(), form.errors.as_text())


class GroupFormTestCase(TestCase):
    def test_group_form_valid(self):
        form_data = {
            'name': 'New Unique Group', 
            'about': 'This is a test group',
        }
        form = GroupForm(data=form_data)
        self.assertTrue(form.is_valid(), msg=form.errors)

    def test_group_form_invalid(self):
        form_data = {
            
        }
        form = GroupForm(data=form_data)
        self.assertFalse(form.is_valid(), msg=form.errors)

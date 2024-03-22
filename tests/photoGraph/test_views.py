import importlib
from django.test import TestCase, RequestFactory, Client

from django.urls import reverse, resolve
from django.contrib import messages
from django.http import JsonResponse, HttpResponseNotFound, HttpResponseBadRequest, HttpResponseForbidden
from django.contrib.auth.models import User
from main.views import *
from main import urls
from main.models import *
from unittest.mock import patch
from django.core.files.uploadedfile import SimpleUploadedFile

# run tests with command - python .\manage.py test tests.photoGraph.test_views
# all test cases pass as of 22/03/2024 14:30

class IndexViewTestCase(TestCase): 
    def test_index_view(self):
        response = self.client.get(reverse('main:index'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'photoGraph/index.html')

    def test_index_mapping_exists(self):
        index_mapping_exists = False

        for url_pattern in urls.urlpatterns:
            if getattr(url_pattern, 'name', '') == 'index':
                index_mapping_exists = True
                break
            
        self.assertTrue(index_mapping_exists)
        self.assertEquals(reverse('main:index'), '/photoGraph/')

class AboutViewTestCase(TestCase): 
    def test_about_view(self):
        response = self.client.get(reverse('main:about'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'photoGraph/about.html')

    def test_index_mapping_exists(self):
        index_mapping_exists = False

        for url_pattern in urls.urlpatterns:
            if getattr(url_pattern, 'name', '') == 'about':
                index_mapping_exists = True
                break
            
        self.assertTrue(index_mapping_exists)
        self.assertEquals(reverse('main:index'), '/photoGraph/')

class ShowUserProfileViewTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='test', password='password123!')
        self.user_profile = UserProfile.objects.create(user=self.user, slug='test-slug')
        
        self.other_user = User.objects.create_user(username='test2', password='password123!')
        self.other_user_profile = UserProfile.objects.create(user=self.other_user, slug='test2-slug')
        
        self.factory = RequestFactory()
    
    def test_user_profile_exists(self):
        response = self.client.get(reverse('main:show_user_profile', args=[self.user_profile.slug]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'photoGraph/user_profile.html')
        self.assertIsNotNone(response.context['user_profile'])
        self.assertEqual(response.context['user_profile'], self.user_profile)
    
    def test_index_mapping_exists(self):
        index_mapping_exists = False

        for url_pattern in urls.urlpatterns:
            if getattr(url_pattern, 'name', '') == 'show_user_profile':
                index_mapping_exists = True
                break
            
        self.assertTrue(index_mapping_exists)
        self.assertEquals(reverse('main:index'), '/photoGraph/')
    
    def test_redirect_for_profile_owner(self):
        self.client.login(username='test', password='password123!')
        response = self.client.get(reverse('main:show_user_profile', args=[self.user_profile.slug]))
        self.assertRedirects(response, reverse('main:my_account'))

class ShowLocationViewTestCase(TestCase):
    @patch('main.models.Post.save', autospec=True)
    def setUp(self, mock_save):
        self.user = User.objects.create_user(username='testuser', password='testpass123!')
        self.user_profile = UserProfile.objects.create(user=self.user)
        self.post = Post.objects.create(created_by=self.user_profile, location_name="Location A", caption="Test", 
                            photo='test_img.jpg' ,latitude = 0.0, longitude=0.0, slug='test', slug_uuid = uuid.uuid4())

    def test_view_with_existing_location(self):
        location_name = 'Location A'
        response = self.client.get(reverse('main:show_location') + f'?location_name={location_name}')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'photoGraph/location.html')
        self.assertEqual(self.post.location_name, 'Location A')

    def test_view_with_non_existing_location(self):
        response = self.client.get(reverse('main:show_location') + '?location_name=no location')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'photoGraph/location.html')
        self.assertNotEqual(self.post.location_name, 'fail')

class ViewPostViewTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass123')
        self.user_profile = UserProfile.objects.create(user=self.user)
        self.post = Post.objects.create(created_by=self.user_profile, slug='test-post', caption="Test Post", photo='test_image.jpg',
                                         latitude=1.1, longitude=1.1)
        Comment.objects.create(created_by=self.user_profile, post=self.post, comment="Test Comment")
        self.client.login(username='testuser', password='testpass123!')


    def test_view_post_with_valid_slug(self):
        response = self.client.get(reverse('main:view_post', args=[self.user_profile.slug, self.post.slug]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'photoGraph/post.html')
        self.assertIsNotNone(response.context['post'])
        self.assertEqual(len(response.context['comments']), 1)
        self.assertFalse(response.context['has_user_liked'])

class CommentViewTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password123!')
        self.user_profile = UserProfile.objects.create(user=self.user)
        self.post = Post.objects.create(created_by=self.user_profile, slug='test-post', caption="Test Post", photo='test_image.jpg',
                                         latitude=1.1, longitude=1.1)        
        self.client.login(username='testuser', password='password123!')
    
    def test_comment_content_by_authenticated_user(self):
        comment_content = 'Test Comment'
        self.client.post(reverse('main:comment', args=[self.post.slug]), {'comment': comment_content})
        new_comment = Comment.objects.first()
        self.assertEqual(new_comment.comment, comment_content)
        self.assertEqual(new_comment.created_by, self.user_profile)
        self.assertEqual(new_comment.post, self.post)

class ShowGroupViewTestCase(TestCase): 
    def setUp(self):
        self.user = User.objects.create_user('testuser', 'test@example.com', 'testpassword')
        self.user_profile = UserProfile.objects.create(user=self.user)
        self.group = Group.objects.create(name="Test Group", slug="test-group", created_by=self.user_profile)
        self.url = reverse('main:show_group', args=[self.group.slug])

    def test_group_exists(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['group'].slug, 'test-group')

    def test_group_does_not_exist(self):
        response = self.client.get(reverse('main:show_group', args=['non-existent-group']))
        self.assertEqual(response.status_code, 200)
        self.assertIsNone(response.context['group'])

    def test_authenticated_user_is_member(self):
        self.group.members.add(self.user_profile)
        another_user = User.objects.create_user('anotheruser', 'another@example.com', 'password123!')
        another_profile = UserProfile.objects.create(user=another_user)
        self.group.members.add(another_profile)

        self.client.login(username='testuser', password='testpassword')  
        response = self.client.get(self.url)
        self.assertTrue(response.context['is_user_member'])

    def test_unauthenticated_user_access(self):
        response = self.client.get(self.url)
        self.assertFalse(response.context['is_user_member'])
        self.assertFalse(response.context['user_is_creator'])

class CreateGroupViewTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', email='test@example.com', password='password123')
        self.user_profile = UserProfile.objects.create(user=self.user)
        self.url = reverse('main:create_group')
    
    def test_redirect_if_not_logged_in(self):
        response = self.client.get(self.url)
        self.assertRedirects(response, f'/photoGraph/login/?next={self.url}')

    
    def test_view_url_exists_at_desired_location(self):
        self.client.login(username='testuser', password='password123')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'photoGraph/create_group.html')
    
    def test_successful_group_creation(self):
        self.client.login(username='testuser', password='password123')
        response = self.client.post(self.url, {'name': 'New Group', 'about': 'This is a test group.'})
        self.assertRedirects(response, reverse("main:show_group_list"))
        self.assertTrue(Group.objects.filter(name='New Group').exists())
    
class JoinGroupViewTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password123!')
        self.user_profile = UserProfile.objects.create(user=self.user)
        self.group = Group.objects.create(name="Test Group", slug="test-group", created_by=self.user_profile)
        self.join_url = reverse('main:join_group')

    def _login(self):
        self.client.login(username='testuser', password='password123!')

    def test_join_group_success(self):
        self._login()
        another_user = User.objects.create_user('anotheruser', 'another@example.com', 'password123!')
        another_profile = UserProfile.objects.create(user=another_user)
        self.group.members.add(another_profile)
        response = self.client.get(self.join_url, {'group_slug': self.group.slug})
        response_data = response.json()
        print(response_data)
        self.assertFalse(response_data["user_in_group"])
        self.assertEqual(response_data["group_size"], 1)

    def test_leave_group_success(self):
        self._login()
        self.group.members.add(self.user_profile)
        response = self.client.get(self.join_url, {'group_slug': self.group.slug})
        response_data = response.json()
        self.assertFalse(response_data["user_in_group"])
        self.assertEqual(response_data["group_size"], 0)

    def test_group_does_not_exist(self):
        self._login()
        response = self.client.get(self.join_url, {'group_slug': 'non-existent-slug'})
        self.assertEqual(response.status_code, HttpResponseNotFound.status_code)

class ShowGroupListViewTestCase(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username='user1', password='password1')
        self.user2 = User.objects.create_user(username='user2', password='password2')
        self.profile1 = UserProfile.objects.create(user=self.user1)
        self.profile2 = UserProfile.objects.create(user=self.user2)
        self.group1 = Group.objects.create(name="Group 1", slug="group-1", created_by=self.profile1)
        self.group2 = Group.objects.create(name="Group 2", slug="group-2", created_by=self.profile2)
        self.group1.members.add(self.profile1, self.profile2)
        self.group2.members.add(self.profile1)
    
    def test_show_group_list_sorted_by_members_count(self):
        response = self.client.get(reverse('main:show_group_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'photoGraph/group_list.html')
        groups = response.context['groups']
        self.assertEqual(groups[0], self.group1)  
        self.assertEqual(groups[1], self.group2) 

    def test_show_group_list_no_groups(self):
        Group.objects.all().delete()
        response = self.client.get(reverse('main:show_group_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'photoGraph/group_list.html')
        self.assertQuerysetEqual(response.context['groups'], [])

class ReportPostViewTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser1', password='password123!')
        self.user_profile = UserProfile.objects.create(user=self.user)
        self.post = Post.objects.create(created_by=self.user_profile, slug='test-post', caption="Test Post", photo='test_image.jpg',
                                         latitude=0.0, longitude=0.0) 
        self.report_url = reverse('main:report_post', kwargs={'post_slug': self.post.slug})

    def test_report_post_view_get(self):
        user = User.objects.create_user(username='testuser2', password='password123')
        self.user_profile = UserProfile.objects.create(user=user)
        self.client.force_login(user)
        response = self.client.get(self.report_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'photoGraph/report_post.html')
    
    def test_report_post_view_post(self):
        user = User.objects.create_user(username='testuser3', password='password123')
        self.user_profile = UserProfile.objects.create(user=user)
        self.client.force_login(user)
        response = self.client.get(self.report_url)
        data = {'reason': 'Inappropriate content'}
        response = self.client.post(self.report_url, data)
        self.assertEqual(response.status_code, 200)
        post_report = PostReport.objects.get(post_id=self.post, reporter=self.user_profile)
        self.assertEqual(post_report.reason, 'Inappropriate content')

    def test_invalid_report_post_view_post(self):
        user = User.objects.create_user(username='testuser4', password='password123')
        self.user_profile = UserProfile.objects.create(user=user)
        self.client.force_login(user)
        response = self.client.get(self.report_url)
        data = {'reason': ''}
        response = self.client.post(self.report_url, data)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'This field is required.')

class ReportDetailViewTestCase(TestCase):
    def setUp(self):
        self.superuser = User.objects.create_superuser(username='admin', email='admin@example.com', password='adminpassword')
        self.user_profile = UserProfile.objects.create(user=self.superuser)
        self.post = Post.objects.create(created_by=self.user_profile, slug='test-post', caption="Test Post", photo='test_image.jpg',
                                         latitude=0.0, longitude=0.0) 
        self.report = PostReport.objects.create(reporter=self.user_profile, post_id=self.post, reason='Inappropriate content')

    def test_report_detail_view(self):
        self.client.force_login(self.superuser)
        response = self.client.get(reverse('main:report_detail', kwargs={'report_id': self.report.id}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'photoGraph/report_detail.html')
        self.assertContains(response, 'Inappropriate content')

    def test_report_detail_view_redirect_non_superuser(self):
        user = User.objects.create_user(username='testuser', password='password123')
        self.client.force_login(user)
        response = self.client.get(reverse('main:report_detail', kwargs={'report_id': self.report.id}))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('main:index'))

    def test_report_detail_view_nonexistent_report_id(self):
        self.client.force_login(self.superuser)
        nonexistent_report_id = self.report.id + 1
        response = self.client.get(reverse('main:report_detail', kwargs={'report_id': nonexistent_report_id}))
        self.assertEqual(response.status_code, 404)

class DeletePostViewTestCase(TestCase):
    def setUp(self):
        self.superuser = User.objects.create_superuser(username='admin', email='admin@example.com', password='adminpassword')
        self.user_profile = UserProfile.objects.create(user=self.superuser)
        self.post = Post.objects.create(created_by=self.user_profile, slug='test-post', caption="Test Post", photo='test_image.jpg',
                                         latitude=1.1, longitude=1.0) 
        self.report = PostReport.objects.create(reporter=self.user_profile, post_id=self.post, reason='Inappropriate content')

    def test_delete_post_view(self):
        self.client.force_login(self.superuser)
        response = self.client.get(reverse('main:delete_post_view', kwargs={'post_id': self.post.id}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'photoGraph/delete_post_report.html')

    def test_delete_post_view_redirect_non_superuser(self):
        user = User.objects.create_user(username='testuser', password='password123')
        self.client.force_login(user)
        response = self.client.get(reverse('main:delete_post_view', kwargs={'post_id': self.post.id}))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('main:index'))

    def test_delete_post_view_post(self):
        self.client.force_login(self.superuser)
        response = self.client.post(reverse('main:delete_post_view', kwargs={'post_id': self.post.id}))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('admin:main_postreport_changelist'))
        self.assertFalse(Post.objects.filter(id=self.post.id).exists())
        self.assertFalse(PostReport.objects.filter(post_id=self.post.id).exists())

    def test_delete_post_view_nonexistent_post_id(self):
        self.client.force_login(self.superuser)
        nonexistent_post_id = self.post.id + 1
        response = self.client.post(reverse('main:delete_post_view', kwargs={'post_id': nonexistent_post_id}))
        self.assertEqual(response.status_code, 404)


class ReportUserViewTestCase(TestCase): 
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password123')
        self.user_profile = UserProfile.objects.create(user=self.user, slug='testuser')
        self.reported_user = User.objects.create_user(username='reporteduser', password='password456')
        self.reported_user_profile = UserProfile.objects.create(user=self.reported_user, slug='reporteduser')

    def test_report_user_view_get(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('main:report_user', kwargs={'user_profile_slug': self.reported_user_profile.slug}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'photoGraph/report_user.html')
        self.assertIn('form', response.context)
        self.assertIsInstance(response.context['form'], UserReportForm)
        self.assertEqual(response.context['reported_user_profile'], self.reported_user_profile)

    def test_report_user_view_post(self):
        self.client.force_login(self.user)
        data = {'reason': 'Inappropriate behavior'}
        response = self.client.post(reverse('main:report_user', kwargs={'user_profile_slug': self.reported_user_profile.slug}), data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'photoGraph/report_user.html')
        self.assertIn('form', response.context)
        self.assertIsInstance(response.context['form'], UserReportForm)
        self.assertIn('show_popup', response.context)
        self.assertTrue(response.context['show_popup'])
        self.assertEqual(UserReport.objects.count(), 1)
        user_report = UserReport.objects.first()
        self.assertEqual(user_report.reporter, self.user_profile)
        self.assertEqual(user_report.user_id, self.reported_user)
        self.assertEqual(user_report.reason, 'Inappropriate behavior')

    def test_report_user_view_invalid_form(self):
        self.client.force_login(self.user)
        data = {'reason': ''}
        response = self.client.post(reverse('main:report_user', kwargs={'user_profile_slug': self.reported_user_profile.slug}), data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'photoGraph/report_user.html')
        self.assertIn('form', response.context)
        self.assertIsInstance(response.context['form'], UserReportForm)
        self.assertNotIn('show_popup', response.context)
        self.assertEqual(UserReport.objects.count(), 0)

class UserReportDetailViewTestCase(TestCase):
    def setUp(self):
        self.superuser = User.objects.create_superuser(username='admin', password='admin123', email='admin@example.com')
        self.user = User.objects.create_user(username='testuser', password='password123')
        self.user_profile = UserProfile.objects.create(user=self.user)
        self.reported_user = User.objects.create_user(username='reporteduser', password='password456')
        self.reported_user_profile = UserProfile.objects.create(user=self.reported_user)
        self.report = UserReport.objects.create(reporter=self.user_profile, user_id=self.reported_user, reason='Test report reason')

    def test_user_report_detail_view_get(self):
        self.client.force_login(self.superuser)
        response = self.client.get(reverse('main:user_report_detail', kwargs={'report_id': self.report.id}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'photograph/user_report_detail.html')
        self.assertIn('report', response.context)
        self.assertEqual(response.context['report'], self.report)
        self.assertIn('reasons', response.context)
        self.assertIsInstance(response.context['reasons'], list)
        self.assertEqual(len(response.context['reasons']), 1)
        self.assertEqual(response.context['reasons'][0], 'Test report reason')

    def test_user_report_detail_view_non_superuser(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('main:user_report_detail', kwargs={'report_id': self.report.id}))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('main:index'))

    def test_user_report_detail_view_invalid_report_id(self):
        self.client.force_login(self.superuser)
        response = self.client.get(reverse('main:user_report_detail', kwargs={'report_id': 999}))
        self.assertEqual(response.status_code, 404)

class DeleteUserViewTestCase(TestCase):
    def setUp(self):
        self.superuser = User.objects.create_superuser(username='admin', password='admin123', email='admin@example.com')
        self.user = User.objects.create_user(username='testuser', password='password123')
        self.user_profile = UserProfile.objects.create(user=self.user)
        self.reported_user = User.objects.create_user(username='reporteduser', password='password456')
        self.reported_user_profile = UserProfile.objects.create(user=self.reported_user)
        self.report = UserReport.objects.create(reporter=self.user_profile, user_id=self.reported_user, reason='Test report reason')

    def test_delete_user_view_get(self):
        self.client.force_login(self.superuser)
        response = self.client.get(reverse('main:delete_user_view', kwargs={'user_id': self.reported_user.id}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'photograph/delete_user_report.html')
        self.assertIn('reported_user', response.context)
        self.assertEqual(response.context['reported_user'], self.reported_user)

    def test_delete_user_view_non_superuser(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('main:delete_user_view', kwargs={'user_id': self.reported_user.id}))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('main:index'))

    def test_delete_user_view_post(self):
        self.client.force_login(self.superuser)
        response = self.client.post(reverse('main:delete_user_view', kwargs={'user_id': self.reported_user.id}))
        self.assertRedirects(response, reverse('admin:main_userreport_changelist'))
        self.assertFalse(User.objects.filter(id=self.reported_user.id).exists())
        self.assertFalse(UserReport.objects.filter(user_id=self.reported_user.id).exists())

    def test_delete_user_view_invalid_user_id(self):
        self.client.force_login(self.superuser)
        response = self.client.get(reverse('main:delete_user_view', kwargs={'user_id': 999}))
        self.assertEqual(response.status_code, 404)

class SignUpViewTestCase(TestCase):
    def test_signup_view_get(self):
        response = self.client.get(reverse('main:signup'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'photoGraph/signup.html')
        self.assertIn('user_form', response.context)
        self.assertIn('profile_form', response.context)

    def test_signup_view_post_valid(self):
        username = 'testuser'
        email = 'test@example.com'
        password = 'testpassword123'

        with open('tests/photoGraph/test_images/test_image.jpg', 'rb') as image_file:
            profile_picture = {
                'profile_picture': SimpleUploadedFile('test_image.jpg', image_file.read(), content_type='image/jpeg'),
            }

        post_data = {
            'username': username,
            'email': email,
            'password': password,
            'confirm_password': password,
            **profile_picture,
            'biography': 'Test biography',
        }
        response = self.client.post(reverse('main:signup'), post_data, format='multipart/form-data')
        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.filter(username=username).exists())
        user = User.objects.get(username=username)
        self.assertEqual(user.username, username)

    def test_signup_view_post_invalid(self):
        post_data = {
            'username': '',
            'email': 'invalidemail',
            'password': '123',
            'confirm_password': '456',
            'profile_picture': '',
            'biography': 'Test biography',
        }

        response = self.client.post(reverse('main:signup'), post_data, format='multipart')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'photoGraph/signup.html')
        self.assertFalse(UserProfile.objects.filter(biography=post_data['biography']).exists())

class LoginPageViewTestCase(TestCase): 
    def setUp(self):
        self.username = 'testuser'
        self.password = 'testpassword123'
        self.user = User.objects.create_user(username=self.username, password=self.password)
        self.client = Client()

    def test_login_page_get(self):
        response = self.client.get(reverse('main:login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'photoGraph/login.html')

    def test_login_page_post_valid(self):
        login_data = {
            'username': self.username,
            'password': self.password,
        }
        response = self.client.post(reverse('main:login'), login_data)
        self.assertEqual(response.status_code, 302) 
        self.assertTrue(response.url.startswith(reverse('main:index')))  

    def test_login_page_post_invalid(self):
        invalid_login_data = {
            'username': 'invalid_username',
            'password': 'invalid_password',
        }
        response = self.client.post(reverse('main:login'), invalid_login_data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'photoGraph/login.html')
        self.assertIn('Invalid login details supplied. Please try again.', response.content.decode())

class PasswordChangeViewTestCase(TestCase):
    def setUp(self):
        self.username = 'testuser'
        self.password = 'oldpassword'
        self.user = User.objects.create_user(username=self.username, password=self.password)
        self.client = Client()

    def test_password_change_view_get(self):
        self.client.login(username=self.username, password=self.password)
        response = self.client.get(reverse('main:passwordChange'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'photoGraph/passwordChange.html')

    def test_password_change_view_post_valid(self):
        self.client.login(username=self.username, password=self.password)
        new_password = 'newpassword123'
        post_data = {
            'old_password': self.password,
            'new_password1': new_password,
            'new_password2': new_password,
        }
        response = self.client.post(reverse('main:passwordChange'), post_data)
        self.assertEqual(response.status_code, 302)  
        self.assertTrue(response.url.startswith(reverse('main:my_account')))  
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password(new_password))  

    def test_password_change_view_post_invalid(self):
        self.client.login(username=self.username, password=self.password)
        invalid_post_data = {
            'old_password': 'wrongpassword',
            'new_password1': 'newpassword123',
            'new_password2': 'newpassword123',
        }
        response = self.client.post(reverse('main:passwordChange'), invalid_post_data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'photoGraph/passwordChange.html')

class InfoChangeViewTestCase(TestCase):
    def setUp(self):
        self.username = 'testuser'
        self.password = 'testpassword123'
        self.user = User.objects.create_user(username=self.username, password=self.password)
        self.user_profile = UserProfile.objects.create(user=self.user)
        self.client = Client()

    def test_info_change_view_get(self):
        self.client.login(username=self.username, password=self.password)
        response = self.client.get(reverse('main:info_change'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'photoGraph/infoChange.html')

    def test_info_change_view_post_valid(self):
        self.client.login(username=self.username, password=self.password)
        new_biography = 'New biography'
        post_data = {
            'biography': new_biography,
        }
        response = self.client.post(reverse('main:info_change'), post_data)
        self.assertEqual(response.status_code, 302) 
        self.assertTrue(response.url.startswith(reverse('main:my_account')))  
        self.user_profile.refresh_from_db()
        self.assertEqual(self.user_profile.biography, new_biography)  

    def test_info_change_view_post_invalid(self):
        self.client.login(username=self.username, password=self.password)
        invalid_post_data = {
            'biography': 'a' * 101,  
        }
        response = self.client.post(reverse('main:info_change'), invalid_post_data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'photoGraph/infoChange.html')

class MyAccountViewTestCase(TestCase):
    def setUp(self):
        self.username = 'testuser'
        self.password = 'testpassword123'
        self.user = User.objects.create_user(username=self.username, password=self.password)
        self.user_profile = UserProfile.objects.create(user=self.user)
        self.client = Client()

    def test_my_account_view_authenticated(self):
        self.client.login(username=self.username, password=self.password)
        response = self.client.get(reverse('main:my_account'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'photoGraph/my_account.html')
        self.assertEqual(response.context['user_profile'], self.user_profile)

    def test_my_account_view_user_posts(self):
        self.client.login(username=self.username, password=self.password)
        post1 = Post.objects.create(created_by=self.user_profile, slug='test-post1', caption="Test Post 1", photo='test_image.jpg',
                                         latitude=0.0, longitude=0.0) 
        post2 = Post.objects.create(created_by=self.user_profile, slug='test-post2', caption="Test Post 2", photo='test_image.jpg',
                                         latitude=1.1, longitude=1.1)
        response = self.client.get(reverse('main:my_account'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'photoGraph/my_account.html')
        self.assertIn(post1, response.context['posts'])
        self.assertIn(post2, response.context['posts'])



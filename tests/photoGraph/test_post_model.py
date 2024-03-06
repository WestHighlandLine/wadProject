from django.test import TestCase
from main.models import Post


class PostModelTestCase(TestCase):

    def test_post_post_time(self):
        import datetime

        time_before = datetime.datetime.now()
        post, post_created = Post.objects.create(latitude=0, longitude=0)
        post.save()
        time_after = datetime.datetime.now()

        self.assertTrue(time_before < post.post_time < time_after)
import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "photoGraph.settings")

import django

django.setup()

from main.models import User, Post, UserProfile, Comment
import random
import lorem  # pip install lorem


def generateComments():
    test_user = User.objects.get_or_create(username="generate_posts_test_user")[0]
    test_user_profile = UserProfile.objects.get_or_create(user=test_user)[0]

    posts = Post.objects.filter(created_by=test_user_profile)

    for post in posts:
        for _ in range(random.randint(0, 3)):
            Comment.objects.create(
                created_by=test_user_profile, post=post, comment=lorem.sentence()
            )


if __name__ == "__main__":
    print("Starting Gavin's comment population script...")
    generateComments()

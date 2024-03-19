import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "photoGraph.settings")

import django

django.setup()

from main.models import Post, UserProfile, Comment
import random
import lorem  # pip install lorem


def generate_comments():
    test_user_profiles = UserProfile.objects.all()
    posts = Post.objects.all()

    for post in posts:
        for _ in range(random.randint(0, 5)):
            test_user_profile = random.choice(test_user_profiles)
            Comment.objects.create(
                created_by=test_user_profile, post=post, comment=lorem.sentence()
            )


def main():
    print("Starting Gavin's comment population script...")
    generate_comments()
    print("Completed Gavin's comment population script.")


if __name__ == "__main__":
    main()

import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "photoGraph.settings")

import django

django.setup()

from main.models import User, UserProfile
import lorem


def generate_users(n=10):
    for i in range(n):
        test_user = User.objects.create(username=f"generate_test_user_{i+1}")
        UserProfile.objects.create(
            user=test_user,
            biography=lorem.paragraph(),
        )


def main():
    print("Starting Gavin's user population script...")
    generate_users()
    print("Completed Gavin's user population script.")


if __name__ == "__main__":
    main()

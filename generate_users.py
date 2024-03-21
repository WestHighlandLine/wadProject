import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "photoGraph.settings")

import django

django.setup()

from main.models import User, UserProfile
import lorem


def generate_users():
    usernames = [
        "MajorNelson",
        "georgeGGs",
        "catlover68",
        "bear_gr1lz",
        "Warringus",
        "McGregor-Ewan",
        "dnd0dungeonmaster",
        "scravistott",
        "chocoEarly",
        "dumbelldoor",
    ]
    for username in usernames:
        test_user = User.objects.create(username=username)
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

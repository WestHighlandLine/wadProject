import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "photoGraph.settings")

import django

django.setup()

from main.models import UserProfile, Group
import random
import lorem


def generate_groups():
    test_user_profiles = list(UserProfile.objects.all())
    group_names = [
        "glasgow-landscapes",
        "gothicArchitecture",
        "greenery",
        "Glaswegian-Core",
        "scottish-tourists-101",
    ]

    for group_name in group_names:
        test_group = Group.objects.create(
            created_by=random.choice(test_user_profiles),
            name=group_name,
            about=lorem.paragraph(),
        )

        n_members = random.randint(1, len(test_user_profiles))
        for test_user_profile in random.sample(test_user_profiles, n_members):
            test_group.members.add(test_user_profile)


def main():
    print("Starting Gavin's group population script...")
    generate_groups()
    print("Completed Gavin's group population script.")


if __name__ == "__main__":
    main()

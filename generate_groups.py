import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "photoGraph.settings")

import django

django.setup()

from main.models import UserProfile, Group, GroupMember
import random
import lorem


def generate_groups(n=5):
    test_user_profiles = UserProfile.objects.all()

    for i in range(n):
        test_group = Group.objects.create(
            created_by=random.choice(test_user_profiles),
            name=f"generate_test_group_{i+1}",
            about=lorem.paragraph,
        )

        possible_group_members = test_user_profiles.copy()
        possible_group_members.remove(test_group.created_by)

        for j in range(random.randint(len(test_user_profiles))):
            test_group_member = GroupMember.objects.create(
                user_profile=random.choice(possible_group_members),
                group=test_group,
            )
            possible_group_members.remove(test_group_member.user_profile)


def main():
    print("Starting Gavin's group population script...")
    generate_groups()
    print("Completed Gavin's group population script.")


if __name__ == "__main__":
    main()

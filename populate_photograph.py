import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "photoGraph.settings")

import django

django.setup()

from django.contrib.auth.models import User
from main.models import UserProfile, Post


def populate():

    users_data = [
        {
            "username": "JoDo",
            "email": "johnDoe@gmail.com",
            "password": "petname123",
        },
        {
            "username": "Gotham_Knight",
            "email": "batman_fan1@gmail.com",
            "password": "ilovechristianbale",
        },
        {
            "username": "RupertH",
            "email": "rupert-humphries@outlook.com",
            "password": "joker-kilt-red",
        },
    ]

    for user_data in users_data:
        user = add_user(**user_data)
        user_profile = add_user_profile(user)

    for user_profile in UserProfile.objects.all():
        print(f"{user_profile} @ {user_profile.slug}")


def add_user(username, email, password):
    user = User.objects.get_or_create(
        username=username, email=email, password=password
    )[0]
    user.save()
    return user


def add_user_profile(user):
    user_profile = UserProfile.objects.get_or_create(user=user)[0]
    user_profile.save()
    return user_profile


if __name__ == "__main__":
    print("Starting photoGraph population script...")
    populate()

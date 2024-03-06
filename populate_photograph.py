import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "photoGraph.settings")

import django

django.setup()

from django.contrib.auth.models import User
from main.models import UserProfile, Post
import datetime


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

    posts_data = [
        {
            "username": "JoDo",
            "caption": "In Paesano Pizza!",
            "latitude": 0,
            "longitude": 0,
        },
        {
            "username": "Gotham_Knight",
            "caption": "me dressed up as Batman",
            "latitude": 0,
            "longitude": 0,
            "about_time": datetime.date(year=2024, month=1, day=1),
        },
        {
            "username": "JoDo",
            "caption": "Walking by the Kelvin.",
            "latitude": 0,
            "longitude": 0,
        },
    ]

    for user_data in users_data:
        user = add_user(**user_data)
        user_profile = add_user_profile(user)

    for user_profile in UserProfile.objects.all():
        print(f"username: {user_profile}\nslug: {user_profile.slug}\n")

    for post_data in posts_data:
        post = add_post(**post_data)

    for post in Post.objects.all():
        print(
            f"username:{post.user_profile}\nslug: {post.slug}\ncaption: {post.caption}\ncoords: ({post.latitude},{post.longitude})\n"
        )


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


def add_post(username, latitude, longitude, caption=None, about_time=None):
    user = User.objects.get(username=username)
    user_profile = UserProfile.objects.get(user=user)
    post = Post.objects.get_or_create(
        user_profile=user_profile,
        latitude=latitude,
        longitude=longitude,
        caption=caption,
        about_time=about_time,
    )[0]
    post.save()
    return post


if __name__ == "__main__":
    print("Starting photoGraph population script...")
    populate()

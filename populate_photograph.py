import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "photoGraph.settings")

import django

django.setup()

from django.contrib.auth.models import User
from main.models import UserProfile, Post, Comment
import datetime


def populate():

    users_data = [
        {
            "username": "JoDo",
            "email": "johnDoe@gmail.com",
            "password": "petname123",
            "posts": [
                {
                    "username": "JoDo",
                    "caption": "In Paesano Pizza!",
                    "latitude": 0,
                    "longitude": 0,
                    "about_time": None,
                    "comments": [
                        {
                            "username": "RupertH",
                            "comment": "Looks delicious!",
                        },
                        {
                            "username": "Gotham_Knight",
                            "comment": "I'm batman.",
                        },
                        {
                            "username": "RupertH",
                            "comment": "On second thought...",
                        },
                    ],
                },
                {
                    "username": "JoDo",
                    "caption": "Walking by the Kelvin.",
                    "latitude": 0,
                    "longitude": 0,
                    "about_time": None,
                    "comments": [],
                },
            ],
        },
        {
            "username": "Gotham_Knight",
            "email": "batman_fan1@gmail.com",
            "password": "ilovechristianbale",
            "posts": [
                {
                    "username": "Gotham_Knight",
                    "caption": "me dressed up as Batman",
                    "latitude": 0,
                    "longitude": 0,
                    "about_time": datetime.date(year=2024, month=1, day=1),
                    "comments": [],
                },
            ],
        },
        {
            "username": "RupertH",
            "email": "rupert-humphries@outlook.com",
            "password": "joker-kilt-red",
            "posts": [],
        },
    ]

    for user_data in users_data:
        user = add_user(user_data)
        user_profile = add_user_profile(user)

        for post_data in user_data["posts"]:
            post = add_post(user_profile, post_data)

            for comment_data in post_data["comments"]:
                comment = add_comment(post, comment_data)

    for user_profile in UserProfile.objects.all():
        print(f"username: {user_profile}\nslug: {user_profile.slug}\n")

    for post in Post.objects.all():
        print(
            f"username:{post.user_profile}\nslug: {post.slug}\ncaption: {post.caption}\ncoords: ({post.latitude},{post.longitude})\n"
        )


def add_user(user_data):
    user = User.objects.get_or_create(
        username=user_data["username"],
        email=user_data["email"],
        password=user_data["password"],
    )[0]
    user.save()
    return user


def add_user_profile(user):
    user_profile = UserProfile.objects.get_or_create(user=user)[0]
    user_profile.save()
    return user_profile


def add_post(user_profile, post_data):
    post = Post.objects.get_or_create(
        user_profile=user_profile,
        latitude=post_data["latitude"],
        longitude=post_data["longitude"],
        caption=post_data["caption"],
        about_time=post_data["about_time"],
    )[0]
    post.save()
    return post


def add_comment(post, comment_data):
    user = User.objects.get(username=comment_data["username"])
    user_profile = UserProfile.objects.get(user=user)

    comment = Comment.objects.get_or_create(
        user_profile=user_profile,
        post=post,
        comment=comment_data["comment"],
    )
    comment.save()
    return comment


if __name__ == "__main__":
    print("Starting photoGraph population script...")
    populate()

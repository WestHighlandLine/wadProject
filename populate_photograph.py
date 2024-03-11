import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "photoGraph.settings")

import django

django.setup()

from django.contrib.auth.models import User
from main.models import UserProfile, Post, Comment


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

    # must add users before comments
    for user_data in users_data:

        for post_data in user_data["posts"]:
            post = add_post(post_data)

            for comment_data in post_data["comments"]:
                comment = add_comment(post, comment_data)

    for user_profile in UserProfile.objects.all():
        print(f"user: {user_profile}\nslug: {user_profile.slug}\n")

    for post in Post.objects.all():
        print(
            f"created_by:{post.created_by}\nslug: {post.slug}\ncaption: {post.caption}\ncoords: ({post.latitude},{post.longitude})\ncreated_time: {post.created_time}\n"
        )

    for comment in Comment.objects.all():
        print(
            f"created_by:{comment.created_by}\ncomment: {comment.comment}\ncreated_time: {comment.created_time}\n"
        )


def add_user(user_data):
    user = User.objects.get_or_create(
        username=user_data["username"],
        email=user_data["email"],
        password=user_data["password"],
    )[0]
    return user


def add_user_profile(user):
    user_profile = UserProfile.objects.get_or_create(user=user)[0]
    return user_profile


def add_post(post_data):
    user = User.objects.get(username=post_data["username"])
    user_profile = UserProfile.objects.get(user=user)

    post = Post.objects.get_or_create(
        created_by=user_profile,
        latitude=post_data["latitude"],
        longitude=post_data["longitude"],
        caption=post_data["caption"],
    )[0]
    return post


def add_comment(post, comment_data):
    user = User.objects.get(username=comment_data["username"])
    user_profile = UserProfile.objects.get(user=user)

    comment = Comment.objects.get_or_create(
        created_by=user_profile,
        post=post,
        comment=comment_data["comment"],
    )[0]
    return comment


if __name__ == "__main__":
    print("Starting Gavin's photoGraph population script...")
    populate()

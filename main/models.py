from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User
import datetime


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    username_slug = models.SlugField(unique=True)
    biography = models.CharField(max_length=100)
    profile_picture = models.ImageField(upload_to="profile_pictures/")

    def save(self, *args, **kwargs):
        self.slug = slugify(self.username)
        super(UserProfile, self).save(*args, **kwargs)

    def __str__(self):
        return self.user.username


class Post(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    caption = models.CharField(max_length=100)
    likes = models.IntegerField(default=0)
    photo = models.ImageField(upload_to="post_photos/")

    latitude = models.FloatField(blank=False)
    longitude = models.FloatField(blank=False)

    aboutTime = models.DateField()
    postTime = models.DateTimeField(editable=False)

    def save(self, *args, **kwargs):
        self.postTime = datetime.datetime.now()
        super(Post, self).save(*args, **kwargs)


class Comment(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    comment = models.CharField(max_length=100)
    commentTime = models.DateTimeField(editable=False)

    def save(self, *args, **kwargs):
        self.commentTime = datetime.datetime.now()
        super(Comment, self).save(*args, **kwargs)


class Group(models.Model):
    userOwner = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
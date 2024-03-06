from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User
import datetime
import http.client
import json


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    username_slug = models.SlugField(unique=True)
    biography = models.CharField(max_length=100)
    profile_picture = models.ImageField(upload_to="profile_pictures/")

    def save(self, *args, **kwargs):
        self.slug = slugify(self.username_slug)
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

    locationName = models.CharField(max_length=100, editable=False, default="Unknown")

    aboutTime = models.DateField()
    postTime = models.DateTimeField(editable=False)

    def save(self, *args, **kwargs):
        self.postTime = datetime.datetime.now()

        # Get a place name from OpenStreetMap API
        try:
            conn = http.client.HTTPSConnection("nominatim.openstreetmap.org")

            # User agent is required so that they don't block us because they don't know what we're doing!
            conn.request("GET", f"/reverse?lat={self.latitude}&lon={self.longitude}&format=json", 
                         headers={"User-Agent": "PhotoGraph/1.0 (University of Glasgow student project)"})

            response = json.loads(conn.getresponse().read())

            self.locationName = response["display_name"]

            print(response)
        except Exception as e:
            print(e)
            self.locationName = f"{self.latitude}, {self.longitude}"

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

class PostReport(models.Model):
    reporter = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    post_id = models.ForeignKey(Post, on_delete=models.CASCADE)
    reason = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Report by {self.reporter.username_slug} on {self.post_id}"
    
    class Meta:
        verbose_name_plural = "Post Reports"
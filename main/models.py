from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User

class UserProfile(models.Model):
    username = models.SlugField(User, on_delete=models.CASCADE, unique=True)
    
    password = models.CharField(max_length=255)  # Assuming encrypted password will be stored
    email = models.EmailField(unique=True)
    description = models.TextField()
    profile_image = models.ImageField(upload_to='profile_images/')
    unique_id = models.UUIDField(primary_key=True, editable=False)
    slug = models.SlugField(unique=True)
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.username)
        super(Category, self).save(*args, **kwargs)    

    def __str__(self):
        return self.user.username

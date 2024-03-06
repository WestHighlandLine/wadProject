from django.contrib import admin
from main.models import UserProfile, Post, PostReport

class PostReportAdmin(admin.ModelAdmin):
    list_display = ['user', 'post', 'reason', 'created_at']
    actions = ['delete_selected']

admin.site.register(UserProfile)
admin.site.register(Post)
admin.site.register(PostReport)

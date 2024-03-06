from django.contrib import admin
from main.models import UserProfile, Post, PostReport
from django.urls import reverse
from django.utils.html import format_html
from django.db.models import Count

class PostReportAdmin(admin.ModelAdmin):
    list_display = ['reporter', 'post_id', 'reason', 'created_at', 'report_count']
    list_display_links = ['post_id']

    def linked_post_id(self, obj):
        post_id_url = reverse('index:view_post', args=[obj.post_id.id])
        return format_html('<a href="{}">{}</a>', post_id_url, obj.post_id.id)
    linked_post_id.short_description = 'Post ID'

    def report_count(self, obj):
        return obj.post_id.postreport_set.count()
    report_count.short_description = 'Report Count'

    #def has_add_permission(self, request):
        #return False
    
    def add_view(self, request, form_url='', extra_context=None):
        extra_context = extra_context or {}
        extra_context['title'] = 'View Post Reports'
        return super().add_view(request, form_url, extra_context)
    
    def change_view(self, request, object_id, form_url='', extra_context=None):
        extra_context = extra_context or {}
        extra_context['show_save'] = False
        extra_context['show_save_and_add_another'] = False
        extra_context['show_save_and_continue'] = False
        return super().change_view(request, object_id, form_url, extra_context)
    
    def get_queryset(self, request):
        # Annotate the queryset with the count of reports for each post
        queryset = super().get_queryset(request)
        queryset = queryset.annotate(report_count=Count('post_id__postreport'))
        return queryset
    
class UserProfileAdmin(admin.ModelAdmin):

    def has_add_permission(self, request):
        return False
    
#class PostAdmin(admin.ModelAdmin):

 #   def has_add_permission(self, request):
  #      return False


admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(Post)
admin.site.register(PostReport, PostReportAdmin)

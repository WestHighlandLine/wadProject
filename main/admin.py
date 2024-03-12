from django.contrib import admin
from main.models import UserProfile, Post, PostReport
from django.urls import reverse
from django.utils.html import format_html
from django.db.models import Count
from django.urls import path
from django.shortcuts import render

class PostReportAdmin(admin.ModelAdmin):
    list_display = ['post_id', 'reason', 'created_at', 'report_count', 'view_report']
    list_filter = ['post_id']

    def post_id(self, obj):
        post_id_url = reverse('main:view_post', args=[obj.post_id.id])
        return format_html('<a href="{}">{}</a>', post_id_url, obj.post_id.id)
    post_id.short_description = 'Post ID'

    def report_count(self, obj):
        return obj.post_id.postreport_set.count()
    report_count.short_description = 'Report Count'

    def view_report(self, obj):
        report_detail_url = reverse('main:report_detail', args=[obj.id])
        return format_html('<a href="{}" class="button" target="_blank">View Report</a>', report_detail_url)
    view_report.short_description = 'View Report'

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('view_report/<int:report_id>/', self.admin_site.admin_view(self.view_report_details), name='view_report'),
        ]
        return custom_urls + urls

    def view_report_details(self, request, report_id):
        report = PostReport.objects.get(id=report_id)
        context = {'report': report}
        return render(request, 'main/view_report_details.html', context)

    def has_add_permission(self, request):
        return False
    
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
    
class PostAdmin(admin.ModelAdmin):

    def has_add_permission(self, request):
        return False
    

admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(PostReport, PostReportAdmin)

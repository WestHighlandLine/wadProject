from django import template
from main.models import Like, UserProfile

register = template.Library()


@register.inclusion_tag("photoGraph/post_template.html")
def post_template(posts=None, show_user_url=True):
    return {"posts": posts, "show_user_url": show_user_url}


@register.inclusion_tag("photoGraph/account_detail_template.html")
def account_detail_template(user_profile=None, show_edit_options=False):
    return {"user_profile": user_profile, "show_edit_options": show_edit_options}


@register.inclusion_tag("photoGraph/comment_template.html")
def comment_template(comments=None):
    return {"comments": comments}


@register.simple_tag
def get_likes(post=None):
    if post != None:
        likes = Like.objects.filter(post=post)
        return len(likes)
    else:
        return 0

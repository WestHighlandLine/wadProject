from django import template

register = template.Library()


@register.inclusion_tag("photoGraph/post_template.html")
def post_template(posts=None):
    return {"posts": posts}


@register.inclusion_tag("photoGraph/account_detail_template.html")
def account_detail_template(user_profile=None, show_edit_options=False):
    return {"user_profile": user_profile, "show_edit_options": show_edit_options}


@register.inclusion_tag("photoGraph/comment_template.html")
def comment_template(comments=None):
    return {"comments": comments}

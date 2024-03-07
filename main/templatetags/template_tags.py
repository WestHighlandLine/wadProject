from django import template

register = template.Library()

@register.inclusion_tag('photoGraph/post_template.html') 
def post_template(posts=None):
    return {"posts": posts}
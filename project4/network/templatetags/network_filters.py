from django import template

register = template.Library()

@register.filter(name='is_liked_by')
def is_liked_by(post, user):
    return post.likes.filter(id=user.id).exists()
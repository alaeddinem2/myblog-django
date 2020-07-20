from django import template

from blog.models import Post , Comment

register=template.Library()
@register.inclusion_tag('blog/latest_posts.html')

def latest_posts():
    context={
        'l_posts':Post.objects.all()[0:5]
    }
    return context

@register.inclusion_tag('blog/latest_comment.html')

def latest_comment():
    context={
        'l_comments':Comment.objects.filter(active=True)[0:5]
    }
    return context
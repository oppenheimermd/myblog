from atexit import register
from django import template
from ..models import Post
from django.db.models import Count
from django.utils.safestring import mark_safe
import markdown

register = template.Library()

@register.filter(name='markdown')
def markdown_format(text):
    return mark_safe(markdown.markdown(text))

@register.simple_tag
def total_posts():
    return Post.published.count()

#   Using an inclusion tag, you can render a template with
#   context variable returned by your tamplate tag
@register.inclusion_tag('blog/post/latest_posts.html')
def show_latest_posts(count=5):
    latest_posts = Post.published.order_by('-publish')[:count]
    #   Note that the function returns a dictionary of varibales instead of
    #   a simple value.  Inclusion tags have to return a dictionary of values
    #   which is used as athe context to render the specified template.
    return {'latest_posts': latest_posts}

#   annotate - QuerySet function to aggregate the total number of comments for
#   each post.  Use Count aggregation function to store the number of comments
#   in the computed field 'total_comments'
@register.simple_tag
def get_most_commented_posts(count=5):
    return Post.published.annotate(
                total_comments=Count('comments')
        ).order_by('-total_comments')[:count]
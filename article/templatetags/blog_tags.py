from django import template
from article.models import Post, Category
from django.db.models import Count
register = template.Library()

@register.inclusion_tag('tags/latest_posts.html')
def songi_postlar():
    posts = Post.objects.filter(status='active').order_by('-created_at')[:5]
    return {'maqolalar':posts}

@register.inclusion_tag('tags/related_posts.html')
def related_posts(ids):
    value = Category.objects.filter(id=ids)
    posts = Post.objects.filter(category__id__in=[c.id for c in value]).order_by('-created_at')[:4]
    return {'posts':posts}

@register.inclusion_tag('tags/most_viewed.html')
def most_viewed():
    posts = Post.objects.filter(status = 'active').order_by('-views')[:7]
    return {'posts':posts}

@register.inclusion_tag('tags/most_comments.html')
def most_comments(count=8):
    posts = Post.objects.annotate(total_comments=Count('izohlar')).order_by('-total_comments')[:count]

    return{'posts':posts}

@register.inclusion_tag('tags/popular_posts.html')
def popular_posts():
    posts = Post.objects.filter(status = 'active').order_by('-views')[:3]
    return {'posts':posts}
        
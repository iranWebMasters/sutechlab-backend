from django import template
from blog.models import Post,Category,Comment
from taggit.models import Tag
register = template.Library()

@register.simple_tag(name='totalposts')
def function():
    posts=Post.objects.filter(status=1).count()
    return posts

@register.simple_tag(name='posts')
def function():
    posts=Post.objects.filter(status=1)
    return posts

@register.filter
def snippet(value,arg=20):
    return value[:20]+". . ."

@register.inclusion_tag('blog/blog-recent-posts.html')
def popularposts():
    posts=Post.objects.filter(status=1).order_by('-published_date')[:3]
    return {'posts': posts}

@register.inclusion_tag('blog/blog-categories.html')
def postcategories():
    posts=Post.objects.filter(status=1)
    categories=Category.objects.all()
    cat_dict={}
    for name in categories:
        cat_dict[name]=posts.filter(category=name).count()
    return{'categories':cat_dict}


@register.simple_tag(name='comment_count')
def function(pid):
    return Comment.objects.filter(post=pid, approved=True).count()

@register.inclusion_tag('blog/blog-tags.html')
def posttags():
    tags = Tag.objects.all()
    return {'tags': tags}
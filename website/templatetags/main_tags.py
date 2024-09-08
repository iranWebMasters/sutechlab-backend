from django import template
from devices.models import Device
from blog.models import Post
from django.utils import timezone
from website.models import Contact,HomePage


register = template.Library()

@register.inclusion_tag('website/index-devices.html')
def display_devices():
    devices=Device.objects.filter(status=1)[0:6]
    return {'devices':devices} 

@register.inclusion_tag('website/index-blog.html')
def display_latest_posts():
    current_time = timezone.now()
    posts=Post.objects.filter(status=1,published_date__lte=current_time).order_by('-published_date')[0:3]
    return {'posts':posts}  

@register.simple_tag
def get_single_contact():
    return Contact.objects.first()

@register.simple_tag
def home_page_data():
    return HomePage.objects.first()

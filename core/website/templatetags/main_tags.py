from django import template
from devices.models import Device
from blog.models import Post
from django.utils import timezone
from website.models import Contact, HomePage, Hyperlink


register = template.Library()


@register.inclusion_tag("website/index-devices.html")
def display_devices():
    devices = Device.objects.filter(display_option="show")[:6]
    return {"devices": devices}


@register.inclusion_tag("website/index-blog.html")
def display_latest_posts():
    current_time = timezone.now()
    posts = Post.objects.filter(
        status=1, display_option="show", published_date__lte=current_time
    ).order_by("-published_date")[0:3]
    return {"posts": posts}


@register.simple_tag
def get_single_contact():
    return Contact.objects.first()


@register.simple_tag
def home_page_data():
    return HomePage.objects.first()


@register.inclusion_tag("website/index-hyperlinks.html")
def display_hyperlinks():
    hyperlinks = Hyperlink.objects.filter(display_option="True")
    return {"hyperlinks": hyperlinks}

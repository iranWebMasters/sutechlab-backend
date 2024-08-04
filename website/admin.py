from django.contrib import admin
from .models import *

class ContactAdmin(admin.ModelAdmin):
    list_display = ('address', 'mobile_phone', 'landline_phone', 'email', 'workingHour') # اضافه شده


class WorkingHourAdmin(admin.ModelAdmin):
    list_display = ('start_day','end_day', 'start_time', 'end_time')

class ContactUsAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone', 'created_date')
    search_fields = ('name', 'email', 'phone', 'message')
    list_filter = ('created_date',)

class NewsletterAdmin(admin.ModelAdmin):
    list_display = ('email',)
    search_fields = ('email',)


class HomePageAdmin(admin.ModelAdmin):
    list_display = ('title',)
    search_fields = ('title',)

class AboutUsAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'title',)
    search_fields = ('title', 'content')
    readonly_fields = ('__str__',)
    summernote_fields = ('content',)



admin.site.register(HomePage, HomePageAdmin)
admin.site.register(ContactUs, ContactUsAdmin)
admin.site.register(Newsletter, NewsletterAdmin)
admin.site.register(WorkingHour, WorkingHourAdmin)
admin.site.register(Contact, ContactAdmin)
admin.site.register(AboutUs, AboutUsAdmin)

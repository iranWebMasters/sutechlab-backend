from django.contrib import admin
from .models import Notification, NotificationLog

class NotificationAdmin(admin.ModelAdmin):
    list_display = ('user', 'title', 'is_read', 'created_at')
    list_filter = ('is_read', 'created_at')
    search_fields = ('title', 'message', 'user__username')  # Assuming User model has a 'username' field
    ordering = ('-created_at',)
    date_hierarchy = 'created_at'

class NotificationLogAdmin(admin.ModelAdmin):
    list_display = ('user', 'notification_type', 'status', 'created_at')
    list_filter = ('notification_type', 'status', 'created_at')
    search_fields = ('message', 'user__username')  # Assuming User model has a 'username' field
    ordering = ('-created_at',)
    date_hierarchy = 'created_at'

# Registering the models with the admin site
admin.site.register(Notification, NotificationAdmin)
admin.site.register(NotificationLog, NotificationLogAdmin)
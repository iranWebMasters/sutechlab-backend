from django.urls import path
from .views import UserNotificationsView, mark_notification_as_read

urlpatterns = [
    path('notifications/', UserNotificationsView.as_view(), name='notifications'),
    path('notifications/read/<int:notification_id>/', mark_notification_as_read, name='mark_notification_as_read'),
]

from django.urls import path
from .views import UserNotificationsView, MarkNotificationAsReadView

app_name = "notifications"


urlpatterns = [
    path("notifications/", UserNotificationsView.as_view(), name="notifications"),
    path(
        "notifications/<int:notification_id>/mark-as-read/",
        MarkNotificationAsReadView.as_view(),
        name="mark_notification_as_read",
    ),
]

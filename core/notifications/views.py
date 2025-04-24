from django.views.generic.list import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from notifications.models import Notification
from django.views import View
from django.http import JsonResponse


class UserNotificationsView(LoginRequiredMixin, ListView):
    model = Notification
    template_name = "userpanel/notifications.html"
    context_object_name = "notifications"

    def get_queryset(self):
        return self.request.user.notifications.all().order_by("-created_at")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["unread_count"] = self.request.user.notifications.filter(
            is_read=False
        ).count()
        return context


class MarkNotificationAsReadView(LoginRequiredMixin, View):
    def post(self, request, notification_id):
        try:
            notification = Notification.objects.get(
                id=notification_id, user=request.user
            )
            notification.is_read = True
            notification.save()
            return JsonResponse({"success": True})
        except Notification.DoesNotExist:
            return JsonResponse(
                {"success": False, "error": "Notification not found"}, status=404
            )

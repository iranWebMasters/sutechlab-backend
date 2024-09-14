from django.urls import path
from .views import *

app_name = 'requests'

urlpatterns = [
    path('', RequestListView.as_view(), name='request-list'),
    path('create/<int:pk>', RequestTemplateView.as_view(), name='request-create'),
    path('<int:pk>/', RequestDetailView.as_view(), name='request-detail'),
]
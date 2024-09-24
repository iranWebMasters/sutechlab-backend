from .views import *
from django.urls import path

app_name = 'api-v1'


urlpatterns = [
    path('page1/<int:pk>/', Page1API.as_view(), name='page-1'),
]

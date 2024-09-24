from .views import *
from django.urls import path

app_name = 'api-v1'


urlpatterns = [
    path('step-1/<int:pk>/', StepOneAPI.as_view(), name='step-1'),
]

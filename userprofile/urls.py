from django.urls import path
from .views import *

app_name = 'profile'

urlpatterns = [
    path('', ProfileIndexview.as_view(), name='index'),
    
]

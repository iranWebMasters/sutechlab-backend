from django.urls import path
from .views import *

app_name = 'userpanel'

urlpatterns = [
    path('', Indexview.as_view(), name='index'),
    
]

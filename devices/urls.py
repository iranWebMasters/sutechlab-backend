from django.urls import path
from .views import *

app_name = 'devices'

urlpatterns = [
    path('', DevicesListView.as_view(), name='index'),
    path('<int:pk>/', DevicesDetailView.as_view(), name='single'),
    path('search/', DevicesSearchView.as_view(), name='search'),
]

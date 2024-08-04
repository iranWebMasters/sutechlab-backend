from django.urls import path
from .views import *

app_name = 'services'

urlpatterns = [
    path('', ServicesListView.as_view(), name='index'),
    path('<int:pk>/', ServicesDetailView.as_view(), name='single'),
    path('search/', ServicesSearchView.as_view(), name='search'),


]

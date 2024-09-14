from .views import *
from django.urls import path

app_name = 'services'


urlpatterns = [
    path('services-api/<int:pk>/', ServicesAPI.as_view(), name='services-api'),
    path('search/', TestSearchView.as_view(), name='search_tests'),
    path('autocomplete/', AutocompleteTestsView.as_view(), name='autocomplete_tests'),
]

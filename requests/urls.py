from django.urls import path
from .views import *

app_name = 'requests'

urlpatterns = [
    path('', RequestListView.as_view(), name='request-list'),
    path('create/', RequestCreateView.as_view(), name='request-create'),
    path('<int:pk>/', RequestDetailView.as_view(), name='request-detail'),
    # path('<int:pk>/update/', RequestUpdateView.as_view(), name='request-update'),
    # path('<int:pk>/delete/', RequestDeleteView.as_view(), name='request-delete'),

    # path('samples/', SampleListView.as_view(), name='sample-list'),
    # path('samples/create/', SampleCreateView.as_view(), name='sample-create'),
    # path('samples/<int:pk>/', SampleDetailView.as_view(), name='sample-detail'),
    # path('samples/<int:pk>/update/', SampleUpdateView.as_view(), name='sample-update'),
    # path('samples/<int:pk>/delete/', SampleDeleteView.as_view(), name='sample-delete'),
]
from django.urls import path
from .views import *

app_name = 'userpanel'

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('profile/update/', ProfileUpdatePanelView.as_view(), name='update_profile_panel'),
    path('experiments/',ExperimentListView.as_view(), name='experiments-list'),
    path('experiments/<int:pk>/',TestDetailView.as_view(), name='experiments-detail'),
]

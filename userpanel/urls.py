from django.urls import path
from .views import *

app_name = 'userpanel'

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('profile/update/', ProfileUpdatePanelView.as_view(), name='update_profile_panel'),
    path('experiments/',ExperimentListView.as_view(), name='experiments-list'),
    path('experiments/<int:pk>/',TestDetailView.as_view(), name='experiments-detail'),

    path('download-invoice/<int:request_id>/', DownloadInvoiceView.as_view(), name='download_invoice'),
    path('delete-request/<int:pk>/', RequestDeleteView.as_view(), name='delete_request'),
    path('edit-request/<int:pk>/', RequestEditView.as_view(), name='edit_request'),

]

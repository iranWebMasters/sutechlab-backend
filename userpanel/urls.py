from django.urls import path
from .views import *

app_name = 'userpanel'

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('profile/update/', ProfileUpdatePanelView.as_view(), name='update_profile_panel'),
    path('experiments/',ExperimentListView.as_view(), name='experiments-list'),
    path('experiments/<int:pk>/',TestDetailView.as_view(), name='experiments-detail'),

    path('download-invoice/<int:request_id>/', DownloadInvoiceView.as_view(), name='download_invoice'),
    path('delete-request/<int:pk>/', LaboratoryRequestDeleteView.as_view(), name='delete_request'),
    path('edit-request/<int:pk>/', RequestEditView.as_view(), name='edit_request'),

    path('requests/<int:pk>/', LaboratoryRequestDetailView.as_view(), name='laboratory_request_detail'),

    path('payment/<int:request_id>/', PaymentPageView.as_view(), name='payment_page'),

    path('payment/process/<int:request_id>/', ProcessPaymentView.as_view(), name='process_payment'),
    path('payment/success/<slug:tracking_code>/', PaymentSuccessView.as_view(), name='payment_success'),

]

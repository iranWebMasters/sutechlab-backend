from django.urls import path
from .views import *

app_name = 'gateway'


urlpatterns = [
    path('payment/gateway/<int:payment_id>/', GoToGatewayView.as_view(), name='payment'),
    path('payment/callback/<int:payment_id>/', CallbackGatewayView.as_view(), name='callback'), 
]

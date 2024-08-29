from django.urls import path
from .views import *

app_name = 'accounts'


urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
    path('profile/update/', ProfileUpdateView.as_view(), name='update_profile'),
]
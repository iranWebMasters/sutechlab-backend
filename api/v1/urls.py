# from .views import *
# from django.urls import path

# app_name = 'api-v1'

# from django.contrib import admin
# from django.urls import path, include
# from rest_framework import permissions
# from drf_yasg.views import get_schema_view
# from drf_yasg import openapi

# schema_view = get_schema_view(
#    openapi.Info(
#       title="Your API Title",
#       default_version='v1',
#       description="This API is created for the registration process of the test request",
#    ),
#    public=True,
#    permission_classes=(permissions.AllowAny,),
# )

# urlpatterns = [
#     path('step-1/<int:pk>/', StepOneAPI.as_view(), name='step-1'),
#     path('step-2/<int:pk>/', StepTwoAPI.as_view(), name='step-2'),
#     path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
#     path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
# ]


from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TemporaryRequestViewSet

router = DefaultRouter()
router.register(r'temporary-requests', TemporaryRequestViewSet)

urlpatterns = [
    path('', include(router.urls)),
]

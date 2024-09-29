from django.contrib import admin
from django.urls import path,include
from django.conf.urls.static import static
from django.conf import settings
from azbankgateways.urls import az_bank_gateways_urls

admin.autodiscover()

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('website.urls')),
    path('devices/', include('devices.urls')),
    path('blog/', include('blog.urls')),
    path('accounts/', include('accounts.urls')),
    path('userpanel/', include('userpanel.urls')),
    path('orders/', include('orders.urls')),
    path('services/', include('services.urls')),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path("bankgateways/", az_bank_gateways_urls()),
    path('gateway/',include('gateway.urls')),
    path('api-auth/', include('rest_framework.urls')),
]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = 'website.views.handler404'
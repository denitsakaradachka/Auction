from django.conf import settings
from django.contrib import admin
from django.urls import path, include, re_path
from django.conf.urls.static import static
from django.views.static import serve

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('auction.common.urls')),
    path('accounts/', include('auction.accounts.urls')),
    path('items/', include('auction.items.urls')),
    path('auctions/', include('auction.auctions.urls')),
    path('tz_detect/', include('tz_detect.urls')),
    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
    re_path(r'^static/(?P<path>.*)$', serve, {'document_root': settings.STATIC_ROOT}),
]

if settings.DEBUG:
    urlpatterns += (
        static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    )

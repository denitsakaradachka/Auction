from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('auction.common.urls')),
    path('accounts/', include('auction.accounts.urls')),
    path('items/', include('auction.items.urls')),
    path('auctions/', include('auction.auctions.urls')),
    path('tz_detect/', include('tz_detect.urls')),
]

if settings.DEBUG:
    urlpatterns += (
        static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    )

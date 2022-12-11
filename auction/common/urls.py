from django.urls import path

from auction.common.views import index, save_auction

urlpatterns = [
    path('', index, name='index'),
    path('save/<int:auction_id>/', save_auction, name='save auction'),
]
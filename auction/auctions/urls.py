from django.urls import path

from auction.auctions.views import start_auction, list_all_auctions, make_bid, auction_details, auctions_for_approval, \
    approve_auction, decline_auction

urlpatterns = [
    path('start/', start_auction, name='start auction'),
    path('', list_all_auctions, name='list all auctions'),
    path('<int:auction_id>/', auction_details, name='auction details'),
    path('<int:auction_id>/bid', make_bid, name='make bid'),
    path('pending', auctions_for_approval, name='pending auctions'),
    path('<int:auction_id>/approve', approve_auction, name='approve auction'),
    path('<int:auction_id>/decline', decline_auction, name='decline auction')
]
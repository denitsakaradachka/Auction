from django.db.models import Count
from django.shortcuts import render, redirect

from auction.auctions.models import Auction, Status
from auction.common.models import AuctionSave


def index(request):
    auctions_with_most_bids = Auction.objects \
                                  .filter(status=Status.approved.value) \
                                  .annotate(bids_count=Count('bid')) \
                                  .order_by('-bids_count')[:6]

    context = {
        'auctions_with_most_bids': auctions_with_most_bids
    }
    return render(request, 'common/home-page.html', context)


def save_auction(request, auction_id):
    user_saved_auction = AuctionSave.objects.filter(auction_id=auction_id, user_id=request.user.pk, )

    if user_saved_auction:
        user_saved_auction.delete()
    else:
        AuctionSave.objects.create(
            auction_id=auction_id,
            user_id=request.user.pk
        )

    return redirect('auction details', auction_id=auction_id)

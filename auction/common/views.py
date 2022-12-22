from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.db.models import Count
from django.http import Http404
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


@login_required
def save_auction(request, auction_id):
    try:
        auction = Auction.objects.filter(pk=auction_id).get()
    except Auction.DoesNotExist as ex:
        raise Http404("Auction does not exist")

    user_saved_auction = AuctionSave.objects.filter(auction_id=auction_id, user_id=request.user.pk, )

    if user_saved_auction:
        user_saved_auction.delete()
    else:
        if request.user == auction.item.user:
            raise PermissionDenied
        AuctionSave.objects.create(
            auction_id=auction_id,
            user_id=request.user.pk
        )

    return redirect(request.META.get('HTTP_REFERER'))
    # return redirect('auction details', auction_id=auction_id)

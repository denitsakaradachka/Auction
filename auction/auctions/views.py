import datetime

from django.contrib.auth.decorators import login_required, permission_required, user_passes_test
from django.shortcuts import render, redirect

from auction.accounts.decorators import group_required
from auction.auctions.forms import StartAuctionForm, MakeBidForm
from auction.auctions.models import Auction, Status
from auction.items.views import item_details


def start_auction(request):
    if request.method != 'POST':
        return redirect('index')

    form = StartAuctionForm(request.POST)
    if form.is_valid():
        auction = form.save(commit=False)
        auction.status = Status.pending.value
        auction.save()

        return redirect('index')

    item_id = form.instance.item.id
    return item_details(request, item_id, submitted_auction_form=form)


def list_all_auctions(request):
    auctions = Auction.objects.filter(status=Status.approved.value).all()

    context = {
        'auctions': auctions
    }
    return render(request, 'auctions/list-all-auctions.html', context)


def auction_details(request, auction_id):
    auction = Auction.objects.filter(pk=auction_id).get()

    context = {
        'auction': auction
    }

    return render(request, 'auctions/auction-details.html', context)


@group_required('moderators')
def auctions_for_approval(request):
    pending_auctions = Auction.objects.filter(status=Status.pending.value).all()

    context = {
        'pending_auctions': pending_auctions
    }

    return render(request, 'accounts/auctions_for_approval.html', context)


@login_required
@permission_required('accounts.can_approve_auction', raise_exception=True)
def approve_auction(request, auction_id):
    auction = Auction.objects.filter(pk=auction_id).get()

    auction.status = Status.approved.value
    auction.save()

    return redirect('pending auctions')


@login_required
@permission_required('accounts.can_approve_auction', raise_exception=True)
def decline_auction(request, auction_id):
    auction = Auction.objects.filter(pk=auction_id).get()

    auction.status = Status.declined.value
    auction.save()

    return redirect('pending auctions')



@login_required
def make_bid(request, auction_id):
    auction = Auction.objects.filter(pk=auction_id).get()

    if auction.is_finished():
        return render(request, 'auctions/auction-finished.html')

    item = auction.item
    highest_bid = auction.bid_set.order_by('-amount').first().amount

    if highest_bid is None:
        highest_bid = auction.start_price

    form = None

    if request.method == 'POST':
        form = MakeBidForm(request.POST)
        if form.is_valid():
            if form.instance.amount <= highest_bid:
                form.add_error('amount', 'Your bid must be higher than the latest one!')
            else:
                bid = form.save(commit=False)
                bid.auction = auction
                bid.user = request.user
                bid.date = datetime.datetime.now()
                bid.save()
                return redirect('auction details', auction_id=auction_id)

    else:
        form = MakeBidForm(initial={'auction': auction_id})

    context = {
        'form': form,
        'auction_id': auction_id,
        'item': item,
        'highest_bid': highest_bid
    }

    return render(request, 'auctions/make-bid.html', context)



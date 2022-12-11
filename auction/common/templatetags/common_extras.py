from django import template

from auction.auctions.models import Auction

register = template.Library()


@register.simple_tag
def is_auction_saved_by_user(auction_id, user_id):
    auction = Auction.objects.filter(pk=auction_id).get()
    return auction.is_saved_by_user(user_id)


@register.simple_tag
def is_current_winner(auction_id, user_id):
    auction = Auction.objects.filter(pk=auction_id).get()
    return auction.latest_bid().user.pk == user_id


@register.simple_tag
def is_auction_owner(auction_id, user_id):
    auction = Auction.objects.filter(pk=auction_id).get()
    return auction.item.user.pk == user_id

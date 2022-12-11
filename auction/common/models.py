from django.contrib.auth import get_user_model
from django.db import models
from django.db.models import RESTRICT

from auction.auctions.models import Auction

UserModel = get_user_model()


class AuctionSave(models.Model):
    auction = models.ForeignKey(
        Auction,
        on_delete=RESTRICT,
        null=False,
        blank=True,
    )

    user = models.ForeignKey(
        UserModel,
        on_delete=models.RESTRICT,
    )

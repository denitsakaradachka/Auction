from datetime import datetime, timezone
from enum import Enum

from django.core.exceptions import ValidationError
from django.db import models

from auction.accounts.models import AppUser, ChoicesEnumMixin
from auction.auctions import validators
from auction.items.models import Item


class Status(ChoicesEnumMixin, Enum):
    pending = 'Pending'
    approved = 'Approved'
    declined = 'Declined'


class Auction(models.Model):

    item = models.OneToOneField(
        Item,
        on_delete=models.RESTRICT,
        null=False,
        blank=False,
        related_name='auction'
    )

    start_datetime = models.DateTimeField(
        null=False,
        blank=False,
        validators=(
            validators.validate_if_start_date_is_in_the_future,
        )

    )

    end_datetime = models.DateTimeField(
        null=False,
        blank=False,

    )

    start_price = models.IntegerField(
        null=False,
        blank=False,

    )

    status = models.CharField(
        null=False,
        blank=True,
        choices=Status.choices(),
        # default=Status.pending,
        max_length=Status.max_len()

    )

    def latest_bid(self):
        return self.bid_set.order_by('-amount').first()

    def bids_count(self):
        return self.bid_set.count()

    def saves_count(self):
        return self.auctionsave_set.count()

    def is_started(self):
        now = datetime.now(timezone.utc)
        utc_start_date = datetime.fromtimestamp(self.start_datetime.timestamp(), tz=timezone.utc)

        return now >= utc_start_date

    def is_finished(self):
        now = datetime.now(timezone.utc)
        utc_end_date = datetime.fromtimestamp(self.end_datetime.timestamp(), tz=timezone.utc)

        return now >= utc_end_date

    def remaining_time(self):
        if self.is_finished():
            return

        now = datetime.now(timezone.utc)
        utc_end_date = datetime.fromtimestamp(self.end_datetime.timestamp(), tz=timezone.utc)

        delta = utc_end_date - now

        all_seconds = delta.seconds

        hours, reminder = divmod(all_seconds, 3600)
        minutes, seconds = divmod(reminder, 60)

        return f'{delta.days} days, {hours:02d}:{minutes:02d}:{seconds:02d} hours'

    def final_date_time(self):
        return self.end_datetime.strftime('%Y/%m/%d %H:%M:%S')

    def clean(self):
        if self.end_datetime <= self.start_datetime:
            raise ValidationError('End date should be after start date.')

        return super(Auction, self).clean()

    def is_saved_by_user(self, user_id):
        found = self.auctionsave_set.filter(user_id=user_id, auction_id=self.pk)
        if found:
            return True
        else:
            return False


class Bid(models.Model):
    user = models.ForeignKey(
        AppUser,
        null=False,
        blank=False,
        on_delete=models.CASCADE
    )

    auction = models.ForeignKey(
        Auction,
        null=False,
        blank=False,
        on_delete=models.CASCADE
    )

    amount = models.IntegerField(
        null=False,
        blank=False,

    )

    date = models.DateTimeField(
        null=False,
        blank=False
    )



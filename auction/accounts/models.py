from enum import Enum

from django.contrib import admin
from django.contrib.auth import models as auth_models
from django.contrib.auth.models import Group
from django.core import validators
from django.db import models

from auction.common.core.validators import validate_only_letters
from auction.items.validators import validate_file_less_than_5mb


class ChoicesEnumMixin:
    @classmethod
    def choices(cls):
        return [(x.name, x.value) for x in cls]

    @classmethod
    def max_len(cls):
        return max(len(name) for name, _ in cls.choices())


class Gender(ChoicesEnumMixin, Enum):
    male = 'Male'
    female = 'Female'
    DoNotShow = 'Do not show'


class AppUser(auth_models.AbstractUser):
    class Meta:
        permissions = (
            ('can_approve_auction', 'Can approve auction'),
        )

    MIN_LEN_FIRST_NAME = 2
    MAX_LEN_FIRST_NAME = 30

    MIN_LEN_LAST_NAME = 2
    MAX_LEN_LAST_NAME = 30

    MAX_LEN_LOCATION = 30

    first_name = models.CharField(
        null=True,
        blank=True,
        max_length=MAX_LEN_FIRST_NAME,
        validators=(
            validators.MinLengthValidator(MIN_LEN_FIRST_NAME),
            validate_only_letters,
        )
    )

    last_name = models.CharField(
        null=True,
        blank=True,
        max_length=MAX_LEN_LAST_NAME,
        validators=(
            validators.MinLengthValidator(MIN_LEN_LAST_NAME),
            validate_only_letters,
        )
    )

    profile_picture = models.ImageField(
        upload_to='profile_photos',
        null=True,
        blank=True,
        validators=(validate_file_less_than_5mb,)
    )

    email = models.EmailField(
        unique=True
    )

    gender = models.CharField(
        choices=Gender.choices(),
        max_length=Gender.max_len()
    )

    location = models.CharField(
        null=False,
        blank=False,
        max_length=MAX_LEN_LOCATION

    )

    def items_count(self):
        return self.item_set.count()

    def auctions_count(self):
        items = self.item_set.all()
        owned_auctions = [item.auction for item in items if hasattr(item, 'auction')]

        return len(owned_auctions)

    def bids_count(self):
        return self.bid_set.count()

    def watchlist_count(self):
        return self.auctionsave_set.count()

    def get_full_name(self):

        if self.first_name is not None and self.last_name is not None:
            return f'{self.first_name} {self.last_name}'

        if self.first_name is not None:
            return self.first_name

        if self.last_name is not None:
            return self.last_name

    def is_moderator(self):
        return bool(self.groups.filter(name='moderators')) or self.is_superuser


from auction.accounts.forms import GroupAdminForm
from django.contrib.auth.admin import GroupAdmin as GroupAdminDefault


# Unregister the original Group admin.
admin.site.unregister(Group)


# Create a new Group admin.
class GroupAdmin(GroupAdminDefault):
    # Use our custom form.
    form = GroupAdminForm
    # Filter permissions horizontal as well.
    filter_horizontal = ['permissions']


# Register the new Group ModelAdmin.
admin.site.register(Group, GroupAdmin)

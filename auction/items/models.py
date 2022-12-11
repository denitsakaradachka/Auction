from enum import Enum

from django.contrib.auth import get_user_model
from django.core import validators
from django.db import models

from auction.accounts.models import ChoicesEnumMixin
from auction.categories.models import Category
from auction.items.validators import validate_file_less_than_5mb

UserModel = get_user_model()


class Condition(ChoicesEnumMixin, Enum):
    unused = 'Unused'
    very_good = 'Very good'
    good = 'Good'
    damaged = 'Damaged'


class Item(models.Model):
    MAX_TITLE_LEN = 30
    MIN_PRICE = 20
    MAX_DESCRIPTION_LEN = 300
    MAX_SPECIFICATIONS_LEN = 200
    MAX_HISTORY_LEN = 300

    title = models.CharField(
        max_length=MAX_TITLE_LEN,
        null=False,
        blank=False,
    )

    item_photo = models.ImageField(
        upload_to='item_photos/',
        null=False,
        blank=True,
        validators=(validate_file_less_than_5mb,),
    )

    approximate_price = models.IntegerField(
        null=True,
        blank=True,
        validators=(
            validators.MinValueValidator(MIN_PRICE),
        )
    )

    description = models.TextField(
        null=False,
        blank=False,
        max_length=MAX_DESCRIPTION_LEN
    )

    specifications = models.TextField(
        null=False,
        blank=False,
        max_length=MAX_SPECIFICATIONS_LEN
    )

    condition = models.CharField(
        null=False,
        blank=False,
        choices=Condition.choices(),
        max_length=Condition.max_len()
    )

    history = models.TextField(
        null=False,
        blank=False,
        max_length=MAX_HISTORY_LEN
    )

    user = models.ForeignKey(
        UserModel,
        on_delete=models.RESTRICT,
        null=False,
        blank=True,
    )

    category = models.ForeignKey(
        Category,
        on_delete=models.RESTRICT,
        null=False,
        blank=False,
    )

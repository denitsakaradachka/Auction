from django.db import models


class Category(models.Model):
    CATEGORY_MAX_LEN = 30

    title = models.CharField(
        null=False,
        blank=False,
        max_length=CATEGORY_MAX_LEN
    )


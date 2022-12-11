import datetime
from django.utils import timezone

from django.core.exceptions import ValidationError


def validate_if_start_date_is_in_the_future(date):
    now = datetime.datetime.now(timezone.utc)
    utc_start_date = datetime.datetime.fromtimestamp(date.timestamp(), tz=timezone.utc)
    if utc_start_date < now:
        raise ValidationError('Start date cannot be in the past.')




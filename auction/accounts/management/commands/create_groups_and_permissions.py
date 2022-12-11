from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission

UserModel = get_user_model()


class Command(BaseCommand):
    help = 'Setup initial groups and permissions for the application'

    def handle(self, *args, **options):
        moderators_group, created = Group.objects.get_or_create(name='moderators')
        if created:
            moderators_group.permissions.add(Permission.objects.get(codename='can_approve_auction'))

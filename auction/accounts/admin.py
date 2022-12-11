from django.contrib import admin

from auction.accounts.models import AppUser


@admin.register(AppUser)
class AppUserAdmin(admin.ModelAdmin):
    pass

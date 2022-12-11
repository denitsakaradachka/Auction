from django.contrib import admin

from auction.categories.models import Category


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    pass

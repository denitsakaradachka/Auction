from django.contrib.auth.decorators import login_required
from django.urls import path

from auction.items.views import ItemCreateView, item_details

urlpatterns = [
    path('add/', login_required(ItemCreateView.as_view()), name='add item'),
    path('<int:item_id>/details/', login_required(item_details), name='details item'),

]
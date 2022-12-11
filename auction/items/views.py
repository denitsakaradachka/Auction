from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView, DetailView

from auction.auctions.forms import StartAuctionForm
from auction.categories.models import Category
from auction.items.forms import ItemCreateForm
from auction.items.models import Item


class ItemsBaseView(View):
    model = Item


class ItemCreateView(ItemsBaseView, CreateView):
    form_class = ItemCreateForm
    template_name = 'items/add_item.html'
    success_url = reverse_lazy('index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


def item_details(request, item_id, submitted_auction_form=None):
    item = Item.objects.filter(pk=item_id, user=request.user).get()
    context = {
        'item': item,
        'start_auction_form': StartAuctionForm(initial={'item': item.id})
    }

    if submitted_auction_form is not None:
        context['submitted_auction_form'] = submitted_auction_form

    return render(request, 'items/details_item.html', context)

# class ItemDetailsView(ItemsBaseView, DetailView):
#     submitted_auction_form = None
#     template_name = 'items/details_item.html'
#
#     def __init__(self, *args, **kwargs):
#         super(ItemDetailsView, self).__init__(*args, **kwargs)
#
#     def get_queryset(self):
#         qs = super(ItemDetailsView, self).get_queryset()
#         return qs.filter(user=self.request.user)
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#
#         start_auction_form = StartAuctionForm(initial={'item': context["item"].id})
#         context['start_auction_form'] = start_auction_form
#
#         if ItemDetailsView.submitted_auction_form is not None:
#             context['submitted_auction_form'] = ItemDetailsView.submitted_auction_form
#
#         return context

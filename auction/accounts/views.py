from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.views import generic as views
from django.shortcuts import render, redirect
from django.contrib.auth import views as auth_views, get_user_model

from auction.accounts.forms import UserCreateForm, LoginForm
from django.views.decorators.http import require_http_methods
from django.contrib.auth import logout as auth_logout

from auction.auctions.models import Bid

UserModel = get_user_model()


class SignInView(auth_views.LoginView):
    template_name = 'accounts/login-page.html'
    form_class = LoginForm
    success_url = reverse_lazy('index')


class SignUpView(views.CreateView):
    template_name = 'accounts/register.html'
    form_class = UserCreateForm
    success_url = reverse_lazy('index')


class SignOutView(auth_views.LogoutView):
    next_page = reverse_lazy('index')


class UserDetailsView(views.DetailView):
    template_name = 'accounts/profile_page.html'
    model = UserModel
    user = get_user_model()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['is_owner'] = self.request.user == self.object
        # context['pets_count'] = self.object.pet_set.count()

        # photos = self.object.photo_set.prefetch_related('photolike_set')
        #
        # context['photos_count'] = photos.count()
        # context['likes_count'] = sum(x.photolike_set.count() for x in photos)

        return context


class UserEditView(views.UpdateView):
    template_name = 'accounts/edit-profile.html'
    model = UserModel
    fields = ('first_name', 'last_name', 'email', 'gender', 'location', 'profile_picture')

    def get_success_url(self):
        return reverse_lazy('details user', kwargs={
            'pk': self.request.user.pk,
        })


@login_required
@require_http_methods(['POST'])
def delete_user(request):
    user_pk = request.user.pk
    auth_logout(request)
    UserModel.objects.filter(pk=user_pk).delete()

    return redirect('index')


@login_required
def my_auctions(request, pk):
    items = request.user.item_set.all()
    owned_auctions = [item.auction for item in items if hasattr(item, 'auction')]

    distinct_bids = Bid.objects.filter(user_id=request.user.pk).distinct('user_id', 'auction_id').all()
    auctions_participations = [bid.auction for bid in distinct_bids]

    context = {
        'owned_auctions': owned_auctions,
        'auctions_participations': auctions_participations
    }

    return render(request, 'accounts/my_auctions.html', context)


@login_required
def my_items(request, pk):
    items = request.user.item_set.all()

    context = {
        'items': items
    }

    return render(request, 'accounts/my_items.html', context)


@login_required
def my_watchlist(request, pk):
    auction_saves = request.user.auctionsave_set.all()
    saved_auctions = [save.auction for save in auction_saves]

    context = {
        'saved_auctions': saved_auctions
    }

    return render(request, 'accounts/my_watchlist.html', context)














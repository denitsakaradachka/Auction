from django.urls import path, include

from auction.accounts.views import SignInView, SignUpView, SignOutView, UserDetailsView, UserEditView, delete_user, \
    my_auctions, my_items, my_watchlist

urlpatterns = [
    path('login/', SignInView.as_view(), name='login user'),
    path('logout/', SignOutView.as_view(), name='logout user'),
    path('register/', SignUpView.as_view(), name='register user'),
    path('delete/', delete_user, name='delete user'),
    path('profile/<int:pk>/', include([
        path('', UserDetailsView.as_view(), name='details user'),
        path('edit/', UserEditView.as_view(), name='edit user'),
        path('auctions/', my_auctions, name='my auctions'),
        path('items/', my_items, name='my items'),
        path('watchlist/', my_watchlist, name='my watchlist')
    ])),
]

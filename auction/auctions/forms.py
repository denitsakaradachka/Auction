from bootstrap_datepicker_plus.widgets import DateTimePickerInput
from django import forms

from auction.auctions.models import Auction, Bid


class StartAuctionForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(StartAuctionForm, self).__init__(*args, **kwargs)
        self.fields['start_price'].label = "Start price"

    class Meta:
        model = Auction
        fields = '__all__'

        widgets = {
            'item': forms.HiddenInput(),
            'start_datetime': DateTimePickerInput(),
            'end_datetime': DateTimePickerInput(),
        }


class MakeBidForm(forms.ModelForm):
    class Meta:
        model = Bid
        fields = ('amount',)

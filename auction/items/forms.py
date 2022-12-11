from django import forms

from auction.items.models import Item


class ItemBaseForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = '__all__'
        # labels = {
        #     'name': 'Pet name',
        #     'personal_photo': 'Link to Image',
        #     'date_of_birth': 'Date of Birth'
        # }
        widgets = {
            'title': forms.TextInput(
                attrs={
                    'placeholder': 'Item title'
                }
            ),
            # 'item_photo': forms.URLInput(
            #     attrs={
            #         'placeholder': 'Link to image'
            #     }
            # ),
            'approximate_price': forms.TextInput(
                attrs={
                    'placeholder': 'Approximate price'
                }
            ),
            'description': forms.Textarea(
                attrs={
                    'placeholder': 'Item description'
                }
            ),
            'specifications': forms.Textarea(
                attrs={
                    'placeholder': 'Item specifications'
                }
            ),
            'history': forms.Textarea(
                attrs={
                    'placeholder': 'Item history'
                }
            ),

        }


class ItemCreateForm(ItemBaseForm):
    pass

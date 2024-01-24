from django import forms

class AuctionItemForm(forms.Form):
    title = forms.CharField(label='Title',required=True, widget=forms.TextInput(attrs={
            'class': 'form-row',
            'placeholder': 'Give it a title'
        })
    )
    description = forms.CharField(label='Description', required=True, widget=forms.Textarea(attrs={
            'class': 'form-row',
            'placeholder': 'Tell more about the product',
            'rows': '3'
        })
    )
    price = forms.DecimalField(label='Price', required=False,initial=0.00,widget=forms.NumberInput(attrs={
            'class': 'form-row',
            'placeholder': 'Estimated price (optional)',
            'min': '0.01',
            'max': '999999999.99',
            'step': '0.01'
        })
    )
    starting_bid = forms.DecimalField(label='Starting Bid', required=True, widget=forms.NumberInput(attrs={
            'class': 'form-row',
            'placeholder': 'Starting bid',
            'min': '0.01',
            'max': '99999999999.99',
            'step': '0.01'
        })
    )
    category = forms.CharField(label='Category', required=False, widget=forms.TextInput(attrs={
            'class': 'form-row',
            'autocomplete': 'on',
            'placeholder': 'Category (optional)'
        })
    )
    image_url = forms.URLField(label='Image URL', required=False, widget=forms.TextInput(attrs={
            'class': 'form-row',
            'placeholder': 'Image URL (optional)',
        })
    )

class CommentForm(forms.Form):
    text = forms.CharField(label='', required=True, widget=forms.Textarea(attrs={
            'class': 'coment-form-text-row',
            'rows': '3',
            'cols': '100',
        })
    )

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super(CommentForm, self).__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()

        # Check if the user is authenticated
        if not self.user.is_authenticated:
            self.add_error('text', "You must be logged in to submit a comment.")
        return cleaned_data

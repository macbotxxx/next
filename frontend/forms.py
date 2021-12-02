from django import forms
from store.models import ReviewRating

class ReviewRatingForm(forms.ModelForm):

    class Meta:
        model = ReviewRating
        fields = ['review', 'rating','subject' ]


class OrderTrackForm(forms.Form):
    tracking_number = forms.CharField(
        max_length=14,
        help_text="Input your order track number , which you can get from order confirmation email.")
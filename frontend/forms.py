from django import forms
from store.models import ReviewRating

class ReviewRatingForm(forms.ModelForm):

    class Meta:
        model = ReviewRating
        fields = ['review', 'rating','subject' ]
from django import forms

from .models import Review


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ("rating", "comment")
        widgets = {
            "rating": forms.NumberInput(attrs={"min": 1, "max": 5}),
            "comment": forms.Textarea(attrs={"rows": 4}),
        }

    def clean_rating(self):
        rating = self.cleaned_data["rating"]

        if rating < 1 or rating > 5:
            raise forms.ValidationError("Rating must be between 1 and 5.")

        return rating
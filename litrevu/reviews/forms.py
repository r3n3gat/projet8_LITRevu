from django import forms
from .models import Ticket, Review, Comment

class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['title', 'description', 'cover_image']
        labels = {
            'title': 'Titre',
            'description': 'Description',
            'cover_image': 'Image',
        }
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
        }

class ReviewForm(forms.ModelForm):
    RATING_CHOICES = [(i, f"{i} ★") for i in range(6)]
    rating = forms.ChoiceField(
        choices=RATING_CHOICES,
        widget=forms.RadioSelect(attrs={'class': 'inline-radio'}),
        label='Note'
    )

    class Meta:
        model = Review
        fields = ['rating', 'headline', 'body']
        labels = {
            'headline': 'Titre',
            'body': 'Commentaire',
        }
        widgets = {
            'body': forms.Textarea(attrs={'rows': 4}),
        }

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['body']
        labels = {'body': 'Commentaire'}
        widgets = {'body': forms.Textarea(attrs={'rows': 3})}

class UserFollowForm(forms.Form):
    username = forms.CharField(label="Nom d’utilisateur")

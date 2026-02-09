from django import forms
from .models import Review, Book


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={
                'rows': 6,
                'placeholder': 'Write your review...',
                'class': 'form-control'
            })
        }
        labels = {
            'content': 'Your Review'
        }


class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'author', 'description', 'cover_url', 'cover_image', 'isbn', 'published_year']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'author': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'rows': 4, 'class': 'form-control'}),
            'cover_url': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'https://...'}),
            'cover_image': forms.FileInput(attrs={'class': 'form-control', 'accept': 'image/*'}),
            'isbn': forms.TextInput(attrs={'class': 'form-control'}),
            'published_year': forms.NumberInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'cover_url': 'Cover Image URL (optional)',
            'cover_image': 'Or Upload Cover Image (optional)',
        }
        help_texts = {
            'cover_url': 'Provide a URL to a cover image',
            'cover_image': 'Or upload an image file directly',
        }

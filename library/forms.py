from django import forms
from .models import Book, Author, Genre


class BookForm(forms.ModelForm):
    # use comma-separated fields for genres and co_authors (temporary names genres_str/co_authors_str)
    class Meta:
        model = Book
        fields = ['title', 'author', 'isbn', 'publication_year', 'genres', 'co_authors', 'summary']
        widgets = {
            'genres': forms.TextInput(attrs={'placeholder': 'genre1, genre2, ...', 'size': 80}),
            'co_authors': forms.TextInput(attrs={'placeholder': 'Author A, Author B', 'size': 80}),
        }

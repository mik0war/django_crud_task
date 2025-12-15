from django.contrib import admin
from .models import Author, Genre, Book


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('id', 'first_name', 'last_name', 'birth_date')
    search_fields = ('first_name', 'last_name')


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'author', 'isbn', 'publication_year')
    search_fields = ('title', 'isbn')
    list_filter = ('publication_year',)

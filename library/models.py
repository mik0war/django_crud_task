from django.db import models


class Author(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    bio = models.TextField(blank=True)
    birth_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Genre(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.ForeignKey(Author, null=True, blank=True, on_delete=models.SET_NULL, related_name='books')
    isbn = models.CharField(max_length=20, unique=True)
    publication_year = models.IntegerField()
    # Comma-separated genres and co-authors as string fields to match the spec
    genres = models.CharField(max_length=500, blank=True)
    co_authors = models.CharField(max_length=500, blank=True)
    summary = models.TextField(blank=True)

    def __str__(self):
        return self.title

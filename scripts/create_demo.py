import os
import django

# Ensure DB env vars are set for this run (override as needed)
os.environ.setdefault('LIBRARY_DB_NAME', 'library_db')
os.environ.setdefault('LIBRARY_DB_USER', 'library_user')
os.environ.setdefault('LIBRARY_DB_PASSWORD', 'LibraryPass2025!')
os.environ.setdefault('LIBRARY_DB_HOST', 'localhost')
os.environ.setdefault('LIBRARY_DB_PORT', '5432')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'library_project.settings')
django.setup()

from django.contrib.auth import get_user_model
from library.models import Author, Genre, Book

User = get_user_model()

def create_superuser():
    if not User.objects.filter(username='admin').exists():
        User.objects.create_superuser('admin', 'admin@example.com', 'adminpass')
        print('Superuser created: admin / adminpass')
    else:
        print('Superuser already exists')

def create_demo_data():
    a1, created = Author.objects.get_or_create(first_name='Leo', last_name='Tolstoy')
    if created:
        print('Author created:', a1)
    a2, created = Author.objects.get_or_create(first_name='Fyodor', last_name='Dostoevsky')
    if created:
        print('Author created:', a2)

    g1, _ = Genre.objects.get_or_create(name='Novel')
    g2, _ = Genre.objects.get_or_create(name='Philosophical')

    book, created = Book.objects.get_or_create(title='War and Peace', defaults={
        'author': a1,
        'isbn': '9780199232765',
        'publication_year': 1869,
        'summary': 'A historical novel.'
    })
    if created:
        book.genres.add(g1)
        book.co_authors.add(a2)
        book.save()
        print('Book created:', book)
    else:
        print('Book already exists:', book)

if __name__ == '__main__':
    create_superuser()
    create_demo_data()

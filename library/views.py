import json
from django.shortcuts import get_object_or_404, redirect, render
from django.views import View
from django.views.generic import ListView
from django.http import JsonResponse, HttpResponseNotAllowed, HttpResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from .models import Book, Author
from .forms import BookForm


class BookListView(ListView):
    model = Book
    template_name = 'library/book_list.html'
    context_object_name = 'books'


class BookCreateView(View):
    def get(self, request):
        form = BookForm()
        return render(request, 'library/book_form.html', {'form': form, 'is_new': True})

    def post(self, request):
        form = BookForm(request.POST)
        if form.is_valid():
            book = form.save()
            return redirect('book_detail', book_id=book.id)
        return render(request, 'library/book_form.html', {'form': form, 'is_new': True})


class BookDetailModifyView(View):
    def get(self, request, book_id):
        book = get_object_or_404(Book, pk=book_id)
        form = BookForm(instance=book)
        return render(request, 'library/book_detail.html', {'book': book, 'form': form})

    def post(self, request, book_id):
        # update existing book
        book = get_object_or_404(Book, pk=book_id)
        # support form POST for updates
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            form.save()
            return redirect('book_detail', book_id=book.id)
        return render(request, 'library/book_detail.html', {'book': book, 'form': form})

    def delete(self, request, book_id):
        book = get_object_or_404(Book, pk=book_id)
        book.delete()
        return JsonResponse({'status': 'deleted'})


@method_decorator(csrf_exempt, name='dispatch')
class AuthorListCreateAPI(View):
    def get(self, request):
        authors = list(Author.objects.values('id', 'first_name', 'last_name', 'bio', 'birth_date'))
        return JsonResponse(authors, safe=False)

    def post(self, request):
        try:
            data = json.loads(request.body.decode('utf-8'))
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
        author = Author.objects.create(
            first_name=data.get('first_name', ''),
            last_name=data.get('last_name', ''),
            bio=data.get('bio', ''),
            birth_date=data.get('birth_date') or None,
        )
        return JsonResponse({'id': author.id, 'first_name': author.first_name, 'last_name': author.last_name, 'bio': author.bio, 'birth_date': str(author.birth_date) if author.birth_date else None}, status=201)


@method_decorator(csrf_exempt, name='dispatch')
class AuthorDetailAPI(View):
    def get(self, request, author_id):
        author = get_object_or_404(Author, pk=author_id)
        data = {'id': author.id, 'first_name': author.first_name, 'last_name': author.last_name, 'bio': author.bio, 'birth_date': str(author.birth_date) if author.birth_date else None}
        return JsonResponse(data)

    def put(self, request, author_id):
        author = get_object_or_404(Author, pk=author_id)
        try:
            data = json.loads(request.body.decode('utf-8'))
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
        author.first_name = data.get('first_name', author.first_name)
        author.last_name = data.get('last_name', author.last_name)
        author.bio = data.get('bio', author.bio)
        birth = data.get('birth_date')
        author.birth_date = birth if birth else None
        author.save()
        return JsonResponse({'id': author.id, 'first_name': author.first_name, 'last_name': author.last_name, 'bio': author.bio, 'birth_date': str(author.birth_date) if author.birth_date else None})

    def delete(self, request, author_id):
        author = get_object_or_404(Author, pk=author_id)
        author.delete()
        return JsonResponse({'status': 'deleted'})

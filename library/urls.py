from django.urls import path
from . import views

urlpatterns = [
    # Book HTML views
    path('books/', views.BookListView.as_view(), name='book_list'),
    path('books/new/', views.BookCreateView.as_view(), name='book_new'),
    # Note: GET/POST/DELETE handled on same pattern for detail/modify
    path('books/<int:book_id>/', views.BookDetailModifyView.as_view(), name='book_detail'),

    # Author JSON API
    path('authors/', views.AuthorListCreateAPI.as_view(), name='author_list_create'),
    path('authors/<int:author_id>/', views.AuthorDetailAPI.as_view(), name='author_detail'),
]

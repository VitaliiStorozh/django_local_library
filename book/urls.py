from django.urls import path
from .views import BooksListViewByAuthor, BooksViewById, BooksViewAll

urlpatterns = [
    path('authors_book/<authors>/', BooksListViewByAuthor.as_view(), name='books_list_url'),
    path('<int:pk>/', BooksViewById.as_view(), name='book_by_id_url'),
    path('', BooksViewAll.as_view(), name='all_books'),
]

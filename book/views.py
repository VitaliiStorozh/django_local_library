from django.http import Http404
from django.shortcuts import get_object_or_404
from django.views.generic import ListView

from author.models import Author
from book.models import Book


class BooksListViewByAuthor(ListView):
    model = Book
    template_name = 'books.html'
    context_object_name = 'books'
    paginate_by = 10

    def get_queryset(self):
        self.authors = get_object_or_404(Author, name=self.kwargs['authors'])
        return Book.objects.filter(authors=self.authors)


class BooksViewById(ListView):
    model = Book
    template_name = 'books.html'
    context_object_name = 'books'
    paginate_by = 10

    def get_queryset(self):
        try:
            return Book.objects.filter(pk=self.kwargs['pk'])
        except Book.DoesNotExist:
            raise Http404("No Books matches the given query.")


class BooksViewAll(ListView):
    model = Book
    template_name = 'books.html'
    context_object_name = 'books'
    paginate_by = 10
    queryset = Book.objects.all()

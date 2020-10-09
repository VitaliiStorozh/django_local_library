from rest_framework import generics, viewsets
from .serializers import BookSerializer
from .models import Book
from rest_framework.permissions import IsAdminUser


class BookView(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    # permission_classes = IsAdminUser
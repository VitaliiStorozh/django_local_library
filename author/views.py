from rest_framework import generics, viewsets
from .serializers import AuthorSerializer
from .models import Author
from rest_framework.permissions import IsAdminUser


class AuthorView(viewsets.ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    # permission_classes = IsAdminUser
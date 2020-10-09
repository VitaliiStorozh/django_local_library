from django.urls import path

from .views import AuthorViewById, AuthorViewAll, delete_author

urlpatterns = [
    path('<int:pk>/', AuthorViewById.as_view(), name='author_by_id_url'),
    path('', AuthorViewAll.as_view(), name='all_author'),
    path("delete/<int:id>/", delete_author, name="delete_author"),
]

from django.http import Http404
from django.shortcuts import redirect
from django.contrib import messages
from django.views.generic import ListView

from authentication.models import CustomUser
from author.models import Author


class AuthorViewById(ListView):
    model = Author
    template_name = 'author.html'
    context_object_name = 'authors'
    paginate_by = 10

    def get_queryset(self):
        try:
            return Author.objects.filter(pk=self.kwargs['pk'])
        except Author.DoesNotExist:
            raise Http404("No Books matches the given query.")


class AuthorViewAll(ListView):
    model = Author
    template_name = 'author.html'
    context_object_name = 'authors'
    paginate_by = 10
    queryset = Author.objects.all()


def delete_author(request, id):
    if not request.user.is_authenticated:
        messages.info(request, "Log in first!")
        return redirect("authorise")
    if not CustomUser.get_by_email(request.user.email).role == 1:
        messages.info(request, "You don`t have permission!")
        return redirect("home")
    Author.delete_by_id(id)
    return redirect("all_author")

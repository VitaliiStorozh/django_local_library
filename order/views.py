from django.contrib import messages
from django.shortcuts import render, redirect
from datetime import datetime, timedelta

from authentication.models import CustomUser
from book.models import Book
from .models import Order


def get_orders(request):
    if not request.user.is_authenticated:
        messages.info(request, "Log in first!")
        return redirect("authorise")
    if CustomUser.get_by_email(request.user.email).role == 1:
        return render(request, "get_orders.html", {"orders": Order.objects.all()})
    return render(request, "get_orders.html", {"orders": Order.objects.all().filter(user_id=request.user.id)})


def new_order(request, id):
    if not request.user.is_authenticated:
        messages.info(request, "Log in first!")
        return redirect("authorise")
    book = Book.get_by_id(id)
    Order.create(request.user, book, datetime.now() + timedelta(days=14))
    messages.info(request, "Order saved!")
    return redirect("home")


def delete_order(request, id):
    if not request.user.is_authenticated:
        messages.info(request, "Log in first!")
        return redirect("authorise")
    Order.delete_by_id(id)
    return redirect("get_orders")

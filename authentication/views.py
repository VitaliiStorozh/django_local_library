from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from .models import CustomUser
from .forms import RegisterForm, AuthoriseForm


def register(request, id=0):
    context = {}
    if request.POST:
        if id == 0:
            form = RegisterForm(request.POST)
        else:
            user = CustomUser.get_by_id(id)
            form = RegisterForm(request.POST, instance=user)
            context["data"] = form
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("home")
        else:
            context["data"] = form
    else:
        if id == 0:
            form = RegisterForm()
        else:
            if not request.user.is_authenticated:
                messages.info(request, "Log in first!")
                return redirect("authorise")
            if not CustomUser.get_by_email(request.user.email).role == 1:
                messages.info(request, "You don`t have permission!")
                return redirect("home")
            user = CustomUser.get_by_id(id)
            form = RegisterForm(instance=user)
        context["data"] = form
    return render(request, "register.html", context=context)


def authorise(request):
    context = {"email": None, "password": None}
    if request.POST:
        form = AuthoriseForm(request.POST)
        email = request.POST.get("email")
        password = request.POST.get("password")
        try:
            user = CustomUser.get_by_email(email)
            if user.check_password(password):
                current_user = authenticate(request, email=email, password=password, role=user.role)
                login(request, current_user)
                return redirect("home")
            else:
                context["data"] = form
                context["password"] = "Incorrect password"
        except ValueError as ve:
            context["email"] = ve
            context["data"] = form
    else:
        form = AuthoriseForm()
        context["data"] = form
    return render(request, "authorise.html", context=context)


def log_out(request):
    logout(request)
    messages.info(request, "Logged out!")
    return redirect("authorise")


def get_all(request):
    if not request.user.is_authenticated:
        messages.info(request, "Log in first!")
        return redirect("authorise")
    if not CustomUser.get_by_email(request.user.email).role == 1:
        messages.info(request, "You don`t have permission!")
        return redirect("home")
    return render(request, "get_users.html", {"users": CustomUser.get_all()})


def delete_user(request, id):
    if not request.user.is_authenticated:
        messages.info(request, "Log in first!")
        return redirect("authorise")
    if not CustomUser.get_by_email(request.user.email).role == 1:
        messages.info(request, "You don`t have permission!")
        return redirect("home")
    CustomUser.delete_by_id(id)
    return redirect("get_users")


def user_info(request, id):
    if not request.user.is_authenticated:
        messages.info(request, "Log in first!")
        return redirect("authorise")
    if not CustomUser.get_by_email(request.user.email).role == 1:
        messages.info(request, "You don`t have permission!")
        return redirect("home")
    return render(request, "get_user_by_id.html", context={"user": CustomUser.get_by_id(id)})


def block(request, id):
    if not request.user.is_authenticated:
        messages.info(request, "Log in first!")
        return redirect("authorise")
    if not CustomUser.get_by_email(request.user.email).role == 1:
        messages.info(request, "You don`t have permission!")
        return redirect("home")
    CustomUser.block(id)
    return redirect("user_info", id)


def change_role(request, id):
    if not request.user.is_authenticated:
        messages.info(request, "Log in first!")
        return redirect("authorise")
    if not CustomUser.get_by_email(request.user.email).role == 1:
        messages.info(request, "You don`t have permission!")
        return redirect("home")
    CustomUser.change_role(id)
    return redirect("user_info", id)


def home(request):
    return render(request, "home.html")

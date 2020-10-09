from authentication.models import CustomUser


def check_is_authenticated(request):
    return request.user.is_authenticated


def check_is_admin(request):
    return CustomUser.get_by_email(request.user.email).role == 1

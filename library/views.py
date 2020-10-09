from re import match

from rest_framework import status
from rest_framework.response import Response


def page_not_found(request, exception=None):
    context = {}
    if match(r"[a-zA-z\d]", str(exception)):
        context["error"] = str(exception)
    else:
        context["error"] = "Resource not found"
    return Response(context, status=status.HTTP_404_NOT_FOUND)


def bad_request(request, exception=None):
    return Response({"exception": "Bad request!!!"}, status=status.HTTP_400_BAD_REQUEST)


def forbidden(request, exception=None):
    return Response({"exception": "You don't have permission!!!"}, status=status.HTTP_403_FORBIDDEN)


def unauthorized(request, exception=None):
    return Response({"exception": "You aren't authorized!!!"}, status=status.HTTP_401_UNAUTHORIZED)

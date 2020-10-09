from django.urls import path
from order import views

urlpatterns = [
    path("", views.get_orders, name="get_orders"),
    path("new_order/<int:id>/", views.new_order, name="new_order"),
    path("delete/<int:id>", views.delete_order, name="delete_order"),
]
from django.urls import path
from order import views

urlpatterns = [
    path('', views.OrderPostGet.as_view()),
    path('<int:order_id>/', views.OrderPutDelete.as_view()),
]

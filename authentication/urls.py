from django.urls import path, include
from rest_framework import routers

import authentication.views as views

router = routers.DefaultRouter()
router.register('', views.UserView)
urlpatterns = [
    path('auth/', include('djoser.urls')),
    path('', include(router.urls)),
    path('<int:id>/', views.UserViewById.as_view()),
    path('<int:id>/orders/', views.UserOrdersPostGet.as_view()),
    path('<int:user_id>/orders/<int:order_id>/', views.UserOrdersPutDelete.as_view()),
]

from rest_framework import viewsets, views, status
from rest_framework.generics import RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import CustomUser
from .serializers import UserSerializer
from library.permissions import IsAdmin, ReadOnly
from order.models import Order
from order.serializers import OrderSerializer


class UserView(viewsets.ModelViewSet):
    queryset = CustomUser.get_all()
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated, IsAdmin,)


class UserViewById(RetrieveUpdateDestroyAPIView):
    queryset = CustomUser.get_all()
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated, ReadOnly | IsAdmin,)


class UserOrdersPostGet(views.APIView):
    queryset = Order.objects.all()
    permission_classes = (IsAuthenticated,)

    def get(self, request, id):
        if not (request.user.id == id or request.user.role == 1):
            return Response({"error": "You don't have permission"}, status=status.HTTP_403_FORBIDDEN)
        try:
            orders = self.queryset.filter(user_id=id)
        except Order.DoesNotExist:
            return Response({"error": "User has no orders yet"}, status=status.HTTP_404_NOT_FOUND)
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)

    def post(self, request, id):
        if not (request.user.id == id or request.user.role == 1):
            return Response({"error": "You don't have permission"}, status=status.HTTP_403_FORBIDDEN)
        try:
            data = {"book": request.data.get("book")[0], "user": id}
        except KeyError:
            return Response({"error": "Bad request"}, status=status.HTTP_400_BAD_REQUEST)
        serializer = OrderSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserOrdersPutDelete(views.APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, user_id, order_id):
        if not (request.user.id == user_id or request.user.role == 1):
            return Response({"error": "You don't have permission"}, status=status.HTTP_403_FORBIDDEN)
        try:
            orders = Order.objects.get(id=order_id, user_id=user_id)
        except Order.DoesNotExist:
            return Response({"error": "User has no orders yet"}, status=status.HTTP_404_NOT_FOUND)
        serializer = OrderSerializer(orders)
        return Response(serializer.data)

    def put(self, request, user_id, order_id):
        if not (request.user.id == user_id or request.user.role == 1):
            return Response({"error": "You don't have permission"}, status=status.HTTP_403_FORBIDDEN)
        data = dict(request.data)
        try:
            data["planned_end_at"] = data["planned_end_at"][0] if data["planned_end_at"][0] else None
            data["end_at"] = data["end_at"][0] if data["end_at"][0] else None
        except KeyError:
            return Response({"error": "Bad request"}, status=status.HTTP_400_BAD_REQUEST)
        order = Order.get_by_id(order_id)
        if not order:
            return Response({"error": "Order isn't found"}, status=status.HTTP_404_NOT_FOUND)
        order.update(data["planned_end_at"], data["end_at"])
        serializer = OrderSerializer(order)
        return Response(serializer.data)

    def delete(self, request, user_id, order_id):
        if not (request.user.id == user_id or request.user.role == 1):
            return Response({"error": "You don't have permission"}, status=status.HTTP_403_FORBIDDEN)

        if not Order.delete_by_id(order_id):
            return Response({"error": "Order isn't found"}, status=status.HTTP_404_NOT_FOUND)
        return Response(status=status.HTTP_204_NO_CONTENT)

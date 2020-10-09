from rest_framework import views, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from order.models import Order
from order.serializers import OrderSerializer


class OrderPostGet(views.APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        if request.user.role == 1:
            serializer = OrderSerializer(Order.get_all(), many=True)
            return Response(serializer.data)
        try:
            orders = Order.get_all().filter(user_id=request.user.id)
        except Order.DoesNotExist:
            return Response({"error": "User has no orders yet"}, status=status.HTTP_404_NOT_FOUND)
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)

    def post(self, request):
        try:
            data = {"book": request.data.get("book")[0], "user": request.user.id}
        except KeyError:
            return Response({"error": "Bad request"}, status=status.HTTP_400_BAD_REQUEST)
        serializer = OrderSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class OrderPutDelete(views.APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, order_id):
        try:
            orders = Order.objects.get(id=order_id)
        except Order.DoesNotExist:
            return Response({"error": "User has no orders yet"}, status=status.HTTP_404_NOT_FOUND)
        if request.user.role == 1:
            serializer = OrderSerializer(orders)
            return Response(serializer.data)
        try:
            orders = orders.filter(user_id=request.user.id)
        except Order.DoesNotExist:
            return Response({"error": "User has no permission to this order"}, status=status.HTTP_403_FORBIDDEN)
        serializer = OrderSerializer(orders)
        return Response(serializer.data)

    def put(self, request, order_id):
        order = Order.get_by_id(order_id)
        if not order:
            return Response({"error": "Order isn't found"}, status=status.HTTP_404_NOT_FOUND)
        if not (request.user.id == order.user_id or request.user.role == 1):
            return Response({"error": "You don't have permission"}, status=status.HTTP_403_FORBIDDEN)
        data = dict(request.data)
        try:
            data["planned_end_at"] = data["planned_end_at"][0] if data["planned_end_at"][0] else None
            data["end_at"] = data["end_at"][0] if data["end_at"][0] else None
        except KeyError:
            return Response({"error": "Bad request"}, status=status.HTTP_400_BAD_REQUEST)
        order.update(data["planned_end_at"], data["end_at"])
        serializer = OrderSerializer(order)
        return Response(serializer.data)

    def delete(self, request, order_id):
        order = Order.get_by_id(order_id)
        if not order:
            return Response({"error": "Order isn't found"}, status=status.HTTP_404_NOT_FOUND)
        if not (request.user.id == order.user_id or request.user.role == 1):
            return Response({"error": "You don't have permission"}, status=status.HTTP_403_FORBIDDEN)
        if not Order.delete_by_id(order_id):
            return Response({"error": "Order isn't found"}, status=status.HTTP_404_NOT_FOUND)
        return Response(status=status.HTTP_204_NO_CONTENT)

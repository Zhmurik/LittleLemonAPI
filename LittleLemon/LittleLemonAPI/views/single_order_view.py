from rest_framework.response import Response
from rest_framework import generics
from rest_framework.views import APIView

from ..models import OrderItem, Order
from ..serializers import OrderItemSerializer, OrderSerializer, OrderSerializerDelivery, OrderSerializerManager


class SingleOrderView(APIView):
    order_items = OrderItem.objects.all()
    order_item_serializer = OrderItemSerializer
    order_serializer = OrderSerializer
    order_serializer_delivery = OrderSerializerDelivery
    order_serializer_manager = OrderSerializerManager

    def get(self, request, *args, **kwargs):
        """
        Returns all items for this order id. If the order ID doesn’t belong to the current user,
        it displays an appropriate HTTP error status code.
        """
        order = Order.objects.filter(pk=kwargs['pk']).first()
        if request.user.groups.filter(name__in=['Manager', 'Delivery crew']).exists() or request.user != order.user:
            return Response({"message": "Access denied"}, 403)
        else:
            order_items = OrderItem.objects.filter(order=order)
            serializer = self.order_item_serializer(order_items, many=True)
            return Response(serializer.data)

    # def put(self, request, *args, **kwargs):
    #     pass

    def patch(self, request, *args, **kwargs):
        """
        Updates the order. A manager can use this endpoint to set a delivery crew to this order, and also update the order status to 0 or 1
        """
        order = Order.objects.filter(pk=kwargs['pk']).first()
        if request.user.groups.filter(name__in=['Manager']).exists():
            serializer = self.order_serializer_manager(order, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, 200)
            return Response(self.order_serializer(order).data, 200)
        elif request.user.groups.filter(name__in=['Delivery crew']).exists():
            serializer = self.order_serializer_delivery(order, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, 200)
        else:
            return Response({"message": "Access denied"}, 403)


    def delete(self, request, *args, **kwargs):
        """
        Deletes this order
        """
        if not request.user.groups.filter(name__in=['Manager']).exists():
            return Response({"message": "Access denied"}, 403)
        order = Order.objects.filter(pk=kwargs['pk']).first()
        order.delete()
        return Response({"message": "Deleted"}, 200)

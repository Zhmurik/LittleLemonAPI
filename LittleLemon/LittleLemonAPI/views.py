from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import MenuItem, OrderItem, Order, Cart
from .serializers import MenuItemSerializer, OrderSerializer, OrderItemSerializer, \
    CartSerializer


class SingleMenuItemView(generics.RetrieveUpdateDestroyAPIView, generics.CreateAPIView):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        if request.user.groups.filter(name='Manager').exists():
            return Response({"message": "Unsupported call"}, 404)
        else:
            return Response({"message": "Access denied"}, 403)

    def put(self, request, *args, **kwargs):
        if request.user.groups.filter(name='Manager').exists():
            return generics.RetrieveUpdateDestroyAPIView.put(self, request, *args, **kwargs)
        else:
            return Response({"message": "Access denied"}, 403)

    def patch(self, request, *args, **kwargs):
        if request.user.groups.filter(name='Manager').exists():
            return generics.RetrieveUpdateDestroyAPIView.patch(self, request, *args, **kwargs)
        else:
            return Response({"message": "Access denied"}, 403)

    def delete(self, request, *args, **kwargs):
        if request.user.groups.filter(name='Manager').exists():
            return generics.RetrieveUpdateDestroyAPIView.delete(self, request, *args, **kwargs)
        else:
            return Response({"message": "Access denied"}, 403)

class MenuItemView(generics.ListCreateAPIView):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        if request.user.groups.filter(name='Manager').exists():
            return generics.ListCreateAPIView.post(self, request, *args, **kwargs)
        else:
            return Response({"message": "Access denied"}, 403)

    def put(self, request, *args, **kwargs):
        return Response({"message": "Access denied"}, 403)

    def patch(self, request, *args, **kwargs):
        return Response({"message": "Access denied"}, 403)

    def delete(self, request, *args, **kwargs):
        return Response({"message": "Access denied"}, 403)

class CartView(generics.ListCreateAPIView, generics.DestroyAPIView):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer

class OrderItemView(generics.RetrieveUpdateDestroyAPIView):
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer

class OrderView(generics.ListCreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
from rest_framework import generics

from ..models import OrderItem
from ..serializers import OrderItemSerializer


class OrderItemView(generics.RetrieveUpdateDestroyAPIView):
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer
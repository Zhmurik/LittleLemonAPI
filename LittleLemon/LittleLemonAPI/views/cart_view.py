from django.contrib import auth
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from ..models import Cart, User
from ..serializers import CartSerializer


class CartView(generics.ListAPIView, generics.CreateAPIView, generics.DestroyAPIView):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Cart.objects.filter(user=user)

    def get(self, request, *args, **kwargs):
        if request.user.groups.filter(name__in=['Manager', 'Delivery crew']).exists():
            return Response({"message": "Access denied"}, 403)
        else:
            return generics.ListCreateAPIView.get(self, request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        if request.user.groups.filter(name__in=['Manager', 'Delivery crew']).exists():
            return Response({"message": "Access denied"}, 403)
        else:
            return generics.CreateAPIView.post(self, request, *args, **kwargs)

    def get_object(self):
        user = self.request.user
        return Cart.objects.filter(user=user)

    def delete(self, request, *args, **kwargs):
        if request.user.groups.filter(name__in=['Manager', 'Delivery crew']).exists():
            return Response({"message": "Access denied"}, 403)
        else:
            return generics.DestroyAPIView.delete(self, request, *args, **kwargs)

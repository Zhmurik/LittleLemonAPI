from django.contrib import auth
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from ..models import Cart, User
from ..serializers import CartSerializer


class CartView(generics.RetrieveDestroyAPIView, generics.CreateAPIView):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        user = self.request.user
        return Cart.objects.filter(user=user).first()

    def get(self, request, *args, **kwargs):
        if request.user.groups.filter(name__in=['Manager', 'Delivery crew']).exists():
            return Response({"message": "Access denied"}, 403)
        else:
            return generics.RetrieveDestroyAPIView.get(self, request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        if request.user.groups.filter(name__in=['Manager', 'Delivery crew']).exists():
            return Response({"message": "Access denied"}, 403)
        else:
            if self.get_object():
                self.destroy(request, *args, **kwargs)
            return generics.CreateAPIView.post(self, request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        if request.user.groups.filter(name__in=['Manager', 'Delivery crew']).exists():
            return Response({"message": "Access denied"}, 403)
        else:
            return generics.RetrieveDestroyAPIView.delete(self, request, *args, **kwargs)

from rest_framework import generics
from rest_framework.throttling import AnonRateThrottle, UserRateThrottle
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from ..models import MenuItem
from ..serializers import MenuItemSerializer


class SingleMenuItemView(generics.RetrieveUpdateDestroyAPIView, generics.CreateAPIView):
    """ Lists single menu item """
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer
    throttle_classes = [AnonRateThrottle, UserRateThrottle]
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

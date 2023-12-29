from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from ..models import MenuItem
from ..serializers import MenuItemSerializer


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

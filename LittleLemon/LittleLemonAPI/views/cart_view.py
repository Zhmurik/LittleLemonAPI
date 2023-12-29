from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from ..models import Cart, User
from ..serializers import CartSerializer


class CartView(generics.ListCreateAPIView, generics.DestroyAPIView):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
    # permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        if request.user.groups.filter(name__in=['Manager', 'Delivery crew']).exists():
            return Response({"message": "Access denied"}, 403)
        else:
            return generics.ListCreateAPIView.get(self, request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        if request.user.groups.filter(name__in=['Manager', 'Delivery crew']).exists():
            return Response({"message": "Access denied"}, 403)
        else:
            return generics.ListCreateAPIView.post(self, request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        if request.user.groups.filter(name__in=['Manager', 'Delivery crew']).exists():
            return Response({"message": "Access denied"}, 403)
        else:
            # get user id from request
            # delete cart based on user id
            # return Response
            # User.objects.get_by_natural_key()
            carts_to_delete = list(self.queryset.filter(user_id=request.user.id))
            ser = CartSerializer(data=carts_to_delete, many=True)
            if ser.is_valid():
                ser.save()
                return Response({ser.data}, 200)
            else:
                return Response({}, 200)

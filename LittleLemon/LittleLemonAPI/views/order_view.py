from django.utils.datetime_safe import datetime
from rest_framework import generics
from rest_framework.views import APIView

from ..models import Order, Cart, User, OrderItem
from ..serializers import OrderSerializer
from rest_framework.response import Response


class OrderView(APIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    '''
    Returns all orders with order items created by this user
    '''
    def get(self, request):
        user = request.user
        if user.groups.filter(name__in=['Manager']).exists():
            orders = self.queryset.all()
        elif request.user.groups.filter(name__in=['Delivery crew']).exists():
            orders = self.queryset.filter(delivery_crew=user)
        else:
            orders = self.queryset.filter(user=user)

        serializer = self.serializer_class(orders, many=True)
        return Response(serializer.data)

    '''
    Creates a new order item for the current user. 
    Gets current cart items from the cart endpoints and adds those items to the order items table. 
    Then deletes all items from the cart for this user.
    '''
    def post(self, request):
        if request.user.groups.filter(name__in=['Manager', 'Delivery crew']).exists():
            return Response({"message": "Access denied"}, 403)
        else:
            user = request.user
            cart = Cart.objects.filter(user=user).first()
            if cart:
                order = Order.objects.create(
                    user=user,
                    delivery_crew=User.objects.filter(groups__name='Delivery crew').first(),
                    total=cart.price,
                    date=datetime.now().date()
                )
                order_item = OrderItem.objects.create(
                    order=order,
                    menuitem=cart.menuitem,
                    quantity=cart.quantity,
                    unit_price=cart.unit_price,
                    price=cart.price
                )
                cart.delete()
                serializer = self.serializer_class(order)
                return Response(serializer.data, 201)
            else:
                return Response({"message": "Please add menu items to a cart"}, 400)

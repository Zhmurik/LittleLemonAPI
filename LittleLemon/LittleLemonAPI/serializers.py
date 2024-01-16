from djoser.conf import User
from rest_framework import serializers
from .models import MenuItem, Cart, Order, OrderItem


class MenuItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = MenuItem
        fields = ['id', 'title', 'price', 'featured', 'category']


class CartSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Cart
        fields = ['id', 'user', 'menuitem', 'quantity', 'unit_price', 'price']
        read_only_fields = ['unit_price', 'price']

    def create(self, validated_data):
        menuitem = MenuItem.objects.get(pk=validated_data['menuitem'].pk)
        cart = Cart(
            user=validated_data['user'],
            menuitem=menuitem,
            quantity=validated_data['quantity'],
            unit_price=menuitem.price,
            price=validated_data['quantity'] * menuitem.price
        )
        cart.save()
        return cart


class OrderSerializer(serializers.ModelSerializer):
    user = serializers.CurrentUserDefault()

    class Meta:
        model = Order
        fields = ["id", 'user', 'delivery_crew', 'status', 'total', 'date']
        read_only_fields = ['total', 'date']


class OrderSerializerDelivery(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Order
        fields = ["id", 'user', 'delivery_crew', 'status', 'total', 'date']
        read_only_fields = ['delivery_crew', 'total', 'date']


class OrderSerializerManager(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Order
        fields = ["id", 'user', 'delivery_crew', 'status', 'total', 'date']
        read_only_fields = ['total', 'date']


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['id', 'order', 'menuitem', 'quantity', 'unit_price', 'price']


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email']



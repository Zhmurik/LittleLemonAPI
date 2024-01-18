import django_filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics
from rest_framework.filters import OrderingFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.throttling import AnonRateThrottle, UserRateThrottle
from rest_framework.response import Response


from ..models import MenuItem
from ..serializers import MenuItemSerializer


class MenuItemFilter(django_filters.FilterSet):
    field_name = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = MenuItem
        fields = '__all__'


class MenuItemView(generics.ListCreateAPIView):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer
    throttle_classes = [AnonRateThrottle, UserRateThrottle]
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = MenuItemFilter
    ordering_fields = ['price']
    ordering = ['title']

    def post(self, request, *args, **kwargs):
        """
        Lists all menu items. Return a 200 – Ok HTTP status code
        """
        if request.user.groups.filter(name='Manager').exists():
            return generics.ListCreateAPIView.post(self, request, *args, **kwargs)
        else:
            return Response({"message": "Access denied"}, 403)

    def put(self, request, *args, **kwargs):
        """ Denies access and returns 403 – Unauthorized HTTP status code """
        return Response({"message": "Access denied"}, 403)

    def patch(self, request, *args, **kwargs):
        return Response({"message": "Access denied"}, 403)

    def delete(self, request, *args, **kwargs):
        return Response({"message": "Access denied"}, 403)

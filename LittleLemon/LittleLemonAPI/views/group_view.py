from django.contrib.auth.models import Group
from djoser.serializers import UserSerializer
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView
from djoser.conf import User


class GroupManagementView(APIView):
    """ Returns all managers """
    """ Assigns the user in the payload to the manager group and returns 201-Created """

    user_queryset = User.objects.all()
    user_serializer = UserSerializer

    def get(self, request):
        if request.user.groups.filter(name__in=['Manager']).exists():
            users = User.objects.filter(groups__name='Manager')
            serializer = self.user_serializer(users, many=True)
            return Response(serializer.data, 200)
        else:
            return Response({"message": "Access denied"}, 403)

    def post(self, request):
        if request.user.groups.filter(name__in=['Manager']).exists():
            user = get_object_or_404(User, username=request.data['username'])
            managers = Group.objects.get(name="Manager")
            managers.user_set.add(user)
            return Response({"message": "Ok"}, 200)
        else:
            return Response({"message": "Access denied"}, 403)


class SingleGroupManagementView(APIView):
    """Removes this particular user from the manager group and returns 200 – Success if everything is okay.
        If the user is not found, returns 404 – Not found """

    user_queryset = User.objects.all()

    def delete(self, request, *args, **kwargs):
        if request.user.groups.filter(name__in=['Manager']).exists():
            user = get_object_or_404(User, pk=kwargs['pk'])
            managers = Group.objects.get(name="Manager")
            managers.user_set.remove(user)
            return Response({"message": "Ok"}, 200)
        else:
            return Response({"message": "Access denied"}, 403)


class GroupDeliveryCrewView(APIView):
    """ Returns all delivery crew"""
    """ Assigns the user in the payload to delivery crew group and returns 201-Created HTTP """

    user_queryset = User.objects.all()
    user_serializer = UserSerializer

    def get(self, request):
        if request.user.groups.filter(name__in=['Manager']).exists():
            users = User.objects.filter(groups__name='Delivery crew')
            serializer = self.user_serializer(users, many=True)
            return Response(serializer.data, 200)
        else:
            return Response({"message": "Access denied"}, 403)

    def post(self, request):
        if request.user.groups.filter(name__in=["Manager"]).exists():
            user = get_object_or_404(User, username=request.data['username'])
            delivery_crew = Group.objects.get(name='Delivery crew')
            delivery_crew.user_set.add(user)
            return Response({"message": "Ok"}, 200)
        else:
            return Response({"message": "Access denied"}, 403)


class SingleGroupDeliveryCrewView(APIView):
    """ Removes this user from the manager group and returns 200 – Success if everything is okay.
        If the user is not found, returns  404 – Not found """
    user_queryset = User.objects.all()

    def delete(self, request, *args, **kwargs):
        if request.user.groups.filter(name__in=["Manager"]).exists():
            user = get_object_or_404(User, pk=kwargs['pk'])
            delivery_crew = Group.objects.get(name="Delivery crew")
            delivery_crew.user_set.remove(user)
            return Response({"message": "Ok"}, 200)
        else:
            return Response({"message": "Access denied"}, 403)

from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework import viewsets
from rest_framework.response import Response

from bestflightUser.models import Profile
from api.v1.serializers import ProfileSerializer
from config.authentication import IsSignUpINOrIsAuthenticated


User = get_user_model()


def coming_up_soon():
    return Response('coming up soon!!!',
                    status=status.HTTP_503_SERVICE_UNAVAILABLE)


class UserViewSet(viewsets.ModelViewSet):
    """You can handle every authentication and user management on your account """ # noqa
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = (IsSignUpINOrIsAuthenticated,)

    def create(self, request):
        """create request payload
        ```{
            "user": {
                "email": "",
                "first_name": "",
                "last_name": "",
                "password": ""
            },
            "photo": null
        }```
        """
        return super(UserViewSet, self).create(request)

    def list(self, request, **kwargs):
        return Response('You can not view a list of users',
                        status=status.HTTP_501_NOT_IMPLEMENTED)

    def retrieve(self, request, pk=None, **kwargs):
        return coming_up_soon()

    def update(self, request, pk=None):
        return coming_up_soon()

    def partial_update(self, request, pk=None):
        return coming_up_soon()

    def destroy(self, request, pk=None):
        return coming_up_soon()

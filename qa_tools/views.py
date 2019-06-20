from django.contrib.auth import get_user_model

from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes

from bestflightUser.tests.factories import ProfileFactory
from config.authentication import IsAdminOnly


@api_view(['POST'])
@permission_classes((IsAdminOnly, ))
def create_test_user(request):
    """this user shall the delete after load testing"""
    profile = ProfileFactory()
    password = get_user_model().objects.make_random_password()
    profile.user.set_password(password)
    profile.user.save()
    return Response({
        'email': profile.user.email,
        'password': password
    }, status=status.HTTP_201_CREATED)

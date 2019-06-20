from datetime import datetime, timedelta

from django.conf import settings
from django.utils import timezone
from django.contrib.auth import get_user_model
from django_filters.rest_framework import DjangoFilterBackend

from rest_framework import status
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated

from bestflightUser.models import Profile
from bestflightApp.models import (
    FlightClass,
    Reservation,
    AvailableFlight,
)
from api.v1.serializers import (
    ProfileSerializer,
    FlightClassSerializer,
    ReservationSerializer,
    AvailableFlightSerializer,
    ProfileSerializerWithoutToken)
from config.authentication import IsSignUpINOrIsAuthenticated


User = get_user_model()


def coming_up_soon():
    return Response('coming up soon!!!',
                    status=status.HTTP_503_SERVICE_UNAVAILABLE)


def failed_login():
    return Response('Wrong email or password.',
                    status=status.HTTP_401_UNAUTHORIZED)


def forbidden():
    return Response('Retrieve action not allowed.',
                    status=status.HTTP_403_FORBIDDEN)


class UserViewSet(viewsets.ModelViewSet):
    """You can handle every authentication and user management on your account """ # noqa
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = (IsSignUpINOrIsAuthenticated,)

    def get_serializer_class(self):
        if self.request.method in ['PATCH', 'PUT']:
            return ProfileSerializerWithoutToken
        return ProfileSerializer

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

    @action(methods=['post'], detail=False)
    def login(self, request, pk=None):
        """login route, via email and password"""
        # check if user is already login
        # we check the type as the route is not protected, so we might get a type of AnonymousUser # noqa
        if type(request.user) is User:
            return Response("Hey, you have an active session already. "
                            "If you still want to login; please logout first.",
                            status=status.HTTP_400_BAD_REQUEST)

        email = request.data.get('email', None)
        password = request.data.get('password', None)

        if not (email or password):
            return Response("Please provide both email and password.",
                            status=status.HTTP_400_BAD_REQUEST)
        try:
            user = User.objects.get(email=email)
            if not user.check_password(password):
                return failed_login()

            # set the pk to the user's profile and call parent class
            profiles = self.get_queryset().filter(user=user)
            if not len(profiles):
                return Response("Something went wrong, you don't have a profile. " # noqa
                                "Please send a support mail to {}.". format(settings.SUPPORT_MAIL),  # noqa
                                status=status.HTTP_424_FAILED_DEPENDENCY)

            return Response(self.get_serializer(profiles.first()).data)
        except User.DoesNotExist:
            return failed_login()

    @action(methods=['post'], detail=False)
    def logout(self, request, pk=None):
        """logout a user, simply delete the token attached to the user"""
        request.user.auth_token.delete()
        return Response(status=status.HTTP_200_OK)

    def retrieve(self, request, pk=None, **kwargs):
        """we would not support retrieve, an admin should use django admin"""
        return forbidden()

    def update(self, request, pk=None, *args, **kwargs):
        # get the profile id from request.user
        profile = self.get_queryset().get(user=request.user)
        request.parser_context['kwargs']['pk'] = profile.id
        return super(UserViewSet, self).update(
            request, pk=profile.id, *args, **kwargs)

    def partial_update(self, request, pk=None, *args, **kwargs):
        # get the profile id from request.user
        profile = self.get_queryset().get(user=request.user)
        request.parser_context['kwargs']['pk'] = profile.id
        return super(UserViewSet, self).partial_update(
            request, pk=profile.id, *args, **kwargs)

    def destroy(self, request, pk=None):
        return coming_up_soon()


class AvailableFlightsViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = AvailableFlightSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('boarding_time', 'cost', 'airlinePath')

    def get_queryset(self):
        """add filter for flight path"""
        pick_up = self.request.query_params.get('from', None)
        destination = self.request.query_params.get('to', None)
        airline = self.request.query_params.get('airline', None)
        minutes_after = datetime.now(tz=timezone.utc) + timedelta(minutes=10)
        queryset = AvailableFlight.objects.filter(
           boarding_time__gt=minutes_after
        )

        if pick_up:
            queryset = queryset.filter(airlinePath__pick_up__icontains=pick_up)
        if destination:
            queryset = queryset.filter(
                airlinePath__destination__icontains=destination)
        if airline:
            queryset = queryset.filter(
                airlinePath__airline__title__icontains=airline)
        return queryset.order_by('id')


class ReservationViewSet(viewsets.ModelViewSet):
    serializer_class = ReservationSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        """show only the user's reservations"""
        return Reservation.objects.filter(
           user=self.request.user
        )

    def partial_update(self, request, pk=None, *args, **kwargs):
        return forbidden()

    def update(self, request, pk=None, *args, **kwargs):
        return forbidden()

    def destroy(self, request, pk=None,):
        return forbidden()


class FlightClassViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = FlightClass.objects.all()
    serializer_class = FlightClassSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('title',)

from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password

from rest_framework import serializers
from rest_framework.authtoken.models import Token

from bestflightUser.models import Profile
from bestflightApp.models import AvailableFlight

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'email', 'first_name', 'last_name', 'password')
        extra_kwargs = {
            'password': {'write_only': True},
            'first_name': {
                'allow_null': False, 'required': True, 'allow_blank': False},
            'last_name': {
                'allow_null': False, 'required': True, 'allow_blank': False},
        }


class ProfileSerializer(serializers.ModelSerializer):
    """serializer Profile object(S)"""
    class Meta:
        model = Profile
        fields = ('user', 'photo', 'international_passport', 'token', 'id')

    user = UserSerializer()
    token = serializers.SerializerMethodField()

    def get_token(self, obj):
        """create auth token for user"""
        app_token, _ = Token.objects.get_or_create(user=obj.user)
        return app_token.key

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user_data['username'] = user_data.get('email')
        user = User.objects.create(**user_data)
        return Profile.objects.create(user=user, **validated_data)


class ProfileSerializerWithoutToken(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = (
            'user', 'photo', 'international_passport', 'dob',
            'international_passport_number', 'id')

    user = UserSerializer()

    def update(self, instance, validated_data):
        """since drf does not handle nested update, we should step up"""
        # update user data
        user = instance.user
        user_data = validated_data.pop('user')
        user.email = user_data.get('email', user.email)
        user.last_name = user_data.get('last_name', user.last_name)
        user.first_name = user_data.get('first_name', user.first_name)
        new_password = user_data.get('password', None)
        user.password = make_password(new_password) if new_password else user.password # noqa
        user.save()

        # update profile data
        instance.dob = validated_data.get('dob', instance.dob)
        instance.photo = validated_data.get('photo', instance.photo)
        instance.international_passport_number = validated_data.get('dob', instance.international_passport_number) # noqa
        instance.international_passport = validated_data.get('international_passport', instance.international_passport) # noqa
        instance.save()
        return instance


class AvailableFlightSerializer(serializers.ModelSerializer):
    class Meta:
        model = AvailableFlight
        fields = (
            'id', 'path', 'boarding_time', 'take_off_time',
            'cost')

    path = serializers.SerializerMethodField()
    cost = serializers.SerializerMethodField()

    def get_path(self, obj):
        return str(obj.airlinePath)

    def get_cost(self, obj):
        return '₦{:,.2f}'.format(obj.cost)

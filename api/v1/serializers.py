from django.contrib.auth import get_user_model

from rest_framework import serializers
from rest_framework.authtoken.models import Token

from bestflightUser.models import Profile

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
        fields = ('user', 'photo', 'international_passport', 'token')

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

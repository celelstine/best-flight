from django.contrib.auth import get_user_model

from rest_framework import permissions
from rest_framework.authentication import TokenAuthentication

User = get_user_model()


class BearerAuthentication(TokenAuthentication):
    keyword = 'Bearer'


class IsSignUpINOrIsAuthenticated(permissions.BasePermission):
    """make only signup and login routes unprotected for obvious reasons :)"""

    def has_permission(self, request, view):
        if not type(request.user) is User:
            if not (view.action == 'create' or view.action == 'login'):
                return False
        return True

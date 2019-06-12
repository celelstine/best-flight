from rest_framework import permissions
from rest_framework.authentication import TokenAuthentication


class BearerAuthentication(TokenAuthentication):
    keyword = 'Bearer'


class IsSignUpINOrIsAuthenticated(permissions.BasePermission):
    """make only signup and login routes unprotected for obvious reasons :)"""

    def has_permission(self, request, view):
        if not request.user:
            if not (view.action == 'create' or view.action == 'login'):
                return False
        return True

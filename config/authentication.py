from rest_framework import permissions
from rest_framework.authentication import TokenAuthentication


class BearerAuthentication(TokenAuthentication):
    keyword = 'Bearer'

class IsSignUpINOrIsAuthenticated(permissions.BasePermission):

    def has_permission(self, request, view):
        if not request.user:
            if  not (view.action == 'create' or view.action == 'retrieve'):
                return False
        return True
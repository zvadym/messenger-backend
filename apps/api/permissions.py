# from rest_framework.exceptions import NotAuthenticated
# from rest_framework.permissions import BasePermission
# from apps.users.models import BlackListedToken
#
#
# class IsTokenValid(BasePermission):
#     message = BlackListedToken.MESSAGE_BLOCKED
#
#     def has_permission(self, request, view):
#         if BlackListedToken.objects.filter(token=request.auth.decode('utf-8')).exists():
#             raise NotAuthenticated
#         return True

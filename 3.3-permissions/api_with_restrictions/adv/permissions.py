from adv.models import Advertisement
from rest_framework.permissions import BasePermission


class IsOwner(BasePermission):

    def has_object_permission(self, request, view, obj):
        return request.user == obj.creator


class IsNotOwner(BasePermission):

    def has_permission(self, request, view):
        pk = view.kwargs.get('pk')
        return request.user != Advertisement.objects.get(id=pk).creator


'''
for future reference:

class IsAdminUs(BasePermission):
    def has_object_permission(self, request, view, obj, superuser_exempt=False):
        a = request.user.id
        check_admin = User.objects.get(id=a)
        if check_admin.is_superuser:
            return True
        return False
'''

from pprint import pprint

from rest_framework.permissions import BasePermission


class IsOwner(BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.user == obj.owner:
            return True
        return False


class IsPleasantHabit(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request:
            pprint(request.data)
            return True
        else:
            return False

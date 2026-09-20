from rest_framework.permissions import BasePermission
from django.contrib.auth.models import AnonymousUser

class AdminPermission(BasePermission):

    def has_permission(self, request, view):
        group_name = "Admin"

        # check all the groups that the user is part of and then see if any of them is Admin
        user = request.user
        
        if request.user is AnonymousUser:
            return False

        user_groups = user.groups.all()
        
        group_names = []
        for group in user_groups:
            group_names.append(group.name)

        print(group_names)
        if group_name in group_names:
            return True

        return False

class ManagerPermission(BasePermission):

    def has_permission(self, request, view):
        group_name = "Manager"

        # check all the groups that the user is part of and then see if any of them is Admin
        user = request.user
        
        if request.user is AnonymousUser:
            return False

        user_groups = user.groups.all()
        
        group_names = []
        for group in user_groups:
            group_names.append(group.name)

        print(group_names)
        if group_name in group_names:
            return True

        return False
from rest_framework import  permissions



class IsSuperAdmin(permissions.BasePermission):


    def has_permission(self, request, view):
        return request.user.user_type=='super_user'
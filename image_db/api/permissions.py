from rest_framework import permissions

class IsAdminUser(permissions.BasePermission):
    """
    Restriction of rights. Actions are available only to the admin or django admin.
    """
    message = 'Не хватает прав, нужны права Администратора'

    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return request.user.is_superuser or request.user.role == 'admin'

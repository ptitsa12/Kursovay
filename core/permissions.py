from rest_framework.permissions import BasePermission, SAFE_METHODS


def user_in_group(user, group_name):
    if not user or not user.is_authenticated:
        return False
    if user.is_superuser:
        return True
    return user.groups.filter(name=group_name).exists()


def user_in_any_group(user, *group_names):
    if not user or not user.is_authenticated:
        return False
    if user.is_superuser:
        return True
    return user.groups.filter(name__in=group_names).exists()


class IsAuthenticatedRole(BasePermission):
    """Базовый класс — только авторизованные."""

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated


class IsManagerOrAdmin(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        return user and user.is_authenticated and (
            user.is_superuser or user.is_staff or user_in_group(user, 'manager')
        )


class IsPurchaserRole(BasePermission):
    def has_permission(self, request, view):
        return user_in_group(request.user, 'purchaser')


class IsStorekeeperRole(BasePermission):
    def has_permission(self, request, view):
        return user_in_group(request.user, 'storekeeper')


class IsAccountantRole(BasePermission):
    def has_permission(self, request, view):
        return user_in_group(request.user, 'accountant')


class IsManagerRole(BasePermission):
    def has_permission(self, request, view):
        return user_in_group(request.user, 'manager')


class IsAdminRole(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        return user and user.is_authenticated and (user.is_superuser or user.is_staff)


class ReadOnly(BasePermission):
    def has_permission(self, request, view):
        return request.method in SAFE_METHODS


def GroupsPermission(*groups):
    """Фабрика permission-класса для списка групп."""

    class _GroupsPermission(BasePermission):
        def has_permission(self, request, view):
            return user_in_any_group(request.user, *groups)

    _GroupsPermission.__name__ = f'GroupsPermission_{"_".join(groups)}'
    return _GroupsPermission

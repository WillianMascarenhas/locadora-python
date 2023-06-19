from rest_framework import permissions
from rest_framework.views import Request, View

from users.models import User


class IsEmployeeOrReadOnly(permissions.BasePermission):
    def has_permission(self, request: Request, view: View) -> bool:
        return (
            request.method in permissions.SAFE_METHODS
            # aqui ele compara se é algum dos metodos especiais como o get, se não for ele vai cair na condição que avalio o token
            or request.user.is_authenticated and request.user.is_employee
            # nesse campo eu passei o employee pq era o campo quer estava usando como comparação, poderia passar is_superuser ou qualquer um outro 
        )
 
class IsUserOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if obj == request.user or request.user.is_employee == True:
            return True

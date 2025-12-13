
from rest_framework import permissions

class IsAuthorOrReadOnly(permissions.BasePermission):
    """
    obyektti tek onin avtori ozgerte aladi, basqalar tek oqiy aladi
    """
    def has_permission(self, request, view):
        # oqiwga ruxsat (GET, HEAD, OPTIONS)
        if request.method in permissions.SAFE_METHODS:
            return True
        # CREATE / POST qiliw - tek login bolganda 
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        # oqiwga har dayim ruxsat bar (GET, HEAD, OPTIONS)
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # Jaziwga tek post tin avtorinagana ruxsat bar
        return obj.author == request.user
    

class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        
        return request.user and request.user.is_staff



class IsAdminOrCreateOnlyOrReadOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        if request.method == 'POST':
            return True
        return request.user and request.user.is_staff




from rest_framework import authentication, permissions
import logging

logger = logging.getLogger("users")


class AdminPermissionMixin:
    """Mixin to enforce admin  only access and session auth"""

    class IsAdminUser(permissions.BasePermission):
        def has_permission(self, request, view):
            user = request.user
            if user and user.is_staff:
                logger.info(
                    "STAFF ACCESS GRANTED: %s", user.email, extra={"request": request}
                )
                return True
            logger.warning("UNAUTHORIZED ACCESS", extra={"request": request})
            return False

    authentication_classes = [authentication.SessionAuthentication]
    # Custom IsAdminUser implemented for additional logging; You can use permissions.IsAdminUser if you want
    permission_classes = [IsAdminUser]


class EligiblePermissionMixin:
    """Mixin to enforce eligible user only access and session auth"""

    class IsEligible(permissions.BasePermission):
        def has_permission(self, request, view):
            user = request.user
            if not user or not user.is_authenticated:
                logger.warning("UNAUTHORIZED ACCESS", extra={"request": request})
                return False

            if user.is_staff:
                logger.info(
                    "STAFF ACCESS GRANTED: %s", user.email, extra={"request": request}
                )
                return True
            if user.is_eligible:
                logger.info(
                    "ACCESS GRANTED: %s", user.email, extra={"request": request}
                )
                return True
            logger.warning("ACCESS DENIED: %s", user.email, extra={"request": request})
            return False

    authentication_classes = [authentication.SessionAuthentication]
    permission_classes = [IsEligible]

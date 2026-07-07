from rest_framework.response import Response
from rest_framework.views import APIView

from . import services
from .exceptions import AppError
from .permissions import HasInternalApiKey


def _require(payload: dict, *fields: str) -> None:
    missing = [field for field in fields if not str(payload.get(field, "")).strip()]
    if missing:
        raise AppError(
            "Validation failed",
            400,
            {"missingFields": missing},
        )


class InternalAaaView(APIView):
    permission_classes = [HasInternalApiKey]

    def permission_denied(self, request, message=None, code=None):
        # Match the Node service's plain 401 (DRF would otherwise downgrade
        # AuthenticationFailed/PermissionDenied to 403 with no auth header set).
        raise AppError("Invalid internal API key", 401)


class AuthenticateView(InternalAaaView):
    def post(self, request):
        payload = request.data
        _require(payload, "nasIpAddress")

        has_username = bool(str(payload.get("username", "")).strip())
        has_mac = bool(services.get_string(payload, services.MAC_ADDRESS_KEYS))
        if not has_username and not has_mac:
            raise AppError(
                "Validation failed",
                400,
                {"missingFields": ["username or callingStationId"]},
            )

        return Response(services.authenticate(payload))


class AuthorizeView(InternalAaaView):
    def post(self, request):
        _require(request.data, "username", "nasIpAddress")
        return Response(services.authorize(request.data))


class AccountingView(InternalAaaView):
    def post(self, request):
        return Response(services.accounting(request.data))


class PostAuthView(InternalAaaView):
    def post(self, request):
        return Response(services.post_auth(request.data))


class DisconnectView(InternalAaaView):
    def post(self, request):
        return Response(services.disconnect(request.data))


class CoaView(InternalAaaView):
    def post(self, request):
        return Response(services.coa(request.data))

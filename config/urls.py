from django.contrib import admin
from django.http import JsonResponse
from django.urls import include, path
from django.utils import timezone


def health(_request):
    return JsonResponse(
        {
            "status": "ok",
            "service": "isp-management-platform",
            "timestamp": timezone.now().isoformat(),
        }
    )


urlpatterns = [
    path("admin/", admin.site.urls),
    path("health", health),
    path("internal/aaa/", include("aaa.urls")),
    path("api/v1/auth/", include("accounts.urls")),
    path("api/v1/billing/", include("billing.urls")),
    path("api/v1/payments/", include("payments.urls")),
]

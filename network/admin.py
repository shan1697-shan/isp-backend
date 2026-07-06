from django.contrib import admin

from .models import NasDevice


@admin.register(NasDevice)
class NasDeviceAdmin(admin.ModelAdmin):
    list_display = ("nas_ip_address", "name", "nas_identifier", "status", "last_seen_at")
    list_filter = ("status",)
    search_fields = ("nas_ip_address", "name", "nas_identifier")

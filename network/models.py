from django.db import models


class NasDevice(models.Model):
    class Status(models.TextChoices):
        ONLINE = "online", "Online"
        OFFLINE = "offline", "Offline"
        UNKNOWN = "unknown", "Unknown"

    nas_ip_address = models.CharField(max_length=64, unique=True, db_index=True)
    nas_identifier = models.CharField(max_length=128, blank=True)
    name = models.CharField(max_length=128, blank=True)
    vendor = models.CharField(max_length=128, blank=True)
    model = models.CharField(max_length=128, blank=True)
    status = models.CharField(
        max_length=16, choices=Status.choices, default=Status.UNKNOWN, db_index=True
    )
    service_types = models.JSONField(default=list, blank=True)
    last_seen_at = models.DateTimeField(null=True, blank=True, db_index=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.name or self.nas_ip_address

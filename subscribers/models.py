from django.db import models

from customers.models import Customer
from plans.models import Plan


class Subscriber(models.Model):
    class ServiceType(models.TextChoices):
        PPPOE = "pppoe", "PPPoE"
        HOTSPOT = "hotspot", "Hotspot"
        STATIC_IP = "static_ip", "Static IP"
        DHCP = "dhcp", "DHCP"

    class Status(models.TextChoices):
        ACTIVE = "active", "Active"
        INACTIVE = "inactive", "Inactive"
        SUSPENDED = "suspended", "Suspended"
        TERMINATED = "terminated", "Terminated"

    subscriber_code = models.CharField(max_length=64, unique=True, db_index=True)
    customer = models.ForeignKey(
        Customer, on_delete=models.PROTECT, related_name="subscribers"
    )
    plan = models.ForeignKey(Plan, on_delete=models.PROTECT, related_name="subscribers")
    username = models.CharField(max_length=128, unique=True, db_index=True)
    password_hash = models.CharField(max_length=255)
    service_type = models.CharField(
        max_length=16, choices=ServiceType.choices, default=ServiceType.PPPOE
    )
    status = models.CharField(
        max_length=16, choices=Status.choices, default=Status.ACTIVE, db_index=True
    )
    expires_at = models.DateTimeField(null=True, blank=True, db_index=True)
    installation_address = models.CharField(max_length=255)
    current_balance = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    suspension_reason = models.CharField(max_length=255, blank=True)
    static_ip_address = models.CharField(max_length=64, blank=True)
    mac_address = models.CharField(max_length=32, blank=True)
    last_online_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True, db_index=True)

    def __str__(self) -> str:
        return f"{self.subscriber_code} - {self.username}"

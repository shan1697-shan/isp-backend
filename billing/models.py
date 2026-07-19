from django.core.serializers.json import DjangoJSONEncoder
from django.db import models

from customers.models import Customer
from plans.models import Plan
from subscribers.models import Subscriber


class BillingSettings(models.Model):
    settings_key = models.CharField(max_length=32, unique=True, default="default")
    invoice_prefix = models.CharField(max_length=16, default="INV")
    default_due_days = models.PositiveIntegerField(default=5)
    grace_period_days = models.PositiveIntegerField(default=3)
    tax_percent = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    suspension_enabled = models.BooleanField(default=True)
    auto_suspend_on_overdue = models.BooleanField(default=False)
    default_billing_day = models.PositiveIntegerField(default=1)
    currency = models.CharField(max_length=8, default="INR")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f"BillingSettings({self.settings_key})"


class BillingAccount(models.Model):
    class Status(models.TextChoices):
        ACTIVE = "active", "Active"
        INACTIVE = "inactive", "Inactive"
        SUSPENDED = "suspended", "Suspended"
        CLOSED = "closed", "Closed"

    account_code = models.CharField(max_length=64, unique=True, db_index=True)
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT, related_name="billing_accounts")
    subscriber = models.OneToOneField(
        Subscriber, on_delete=models.CASCADE, related_name="billing_account"
    )
    plan = models.ForeignKey(Plan, on_delete=models.PROTECT, related_name="billing_accounts")
    status = models.CharField(
        max_length=16, choices=Status.choices, default=Status.ACTIVE, db_index=True
    )
    outstanding_balance = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    billing_day = models.PositiveIntegerField(default=1)
    due_days = models.PositiveIntegerField(default=5)
    grace_period_days = models.PositiveIntegerField(default=3)
    suspension_enabled = models.BooleanField(default=True)
    auto_generate_invoices = models.BooleanField(default=True)
    notes = models.CharField(max_length=255, blank=True)
    last_invoice_at = models.DateTimeField(null=True, blank=True)
    next_invoice_date = models.DateTimeField(null=True, blank=True)
    deleted_at = models.DateTimeField(null=True, blank=True, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.account_code


class Invoice(models.Model):
    class Status(models.TextChoices):
        DRAFT = "draft", "Draft"
        ISSUED = "issued", "Issued"
        PARTIALLY_PAID = "partially_paid", "Partially Paid"
        PAID = "paid", "Paid"
        OVERDUE = "overdue", "Overdue"
        VOID = "void", "Void"
        CANCELLED = "cancelled", "Cancelled"

    invoice_number = models.CharField(max_length=64, unique=True, db_index=True)
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT, related_name="invoices")
    subscriber = models.ForeignKey(Subscriber, on_delete=models.PROTECT, related_name="invoices")
    plan = models.ForeignKey(Plan, on_delete=models.PROTECT, related_name="invoices")
    billing_period_start = models.DateTimeField()
    billing_period_end = models.DateTimeField()
    due_date = models.DateTimeField(db_index=True)
    subtotal = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    tax_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    balance_due = models.DecimalField(max_digits=12, decimal_places=2)
    status = models.CharField(
        max_length=16, choices=Status.choices, default=Status.ISSUED, db_index=True
    )
    notes = models.CharField(max_length=255, blank=True)
    line_items = models.JSONField(default=list, encoder=DjangoJSONEncoder)
    deleted_at = models.DateTimeField(null=True, blank=True, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.invoice_number


class LedgerEntry(models.Model):
    class EntryType(models.TextChoices):
        INVOICE = "invoice", "Invoice"
        PAYMENT = "payment", "Payment"
        ADJUSTMENT = "adjustment", "Adjustment"

    customer = models.ForeignKey(Customer, on_delete=models.PROTECT, related_name="ledger_entries")
    subscriber = models.ForeignKey(
        Subscriber, on_delete=models.PROTECT, related_name="ledger_entries"
    )
    invoice = models.ForeignKey(
        Invoice, on_delete=models.SET_NULL, null=True, blank=True, related_name="ledger_entries"
    )
    payment = models.ForeignKey(
        "payments.Payment",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="ledger_entries",
    )
    entry_type = models.CharField(max_length=16, choices=EntryType.choices, db_index=True)
    debit = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    credit = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    balance_impact = models.DecimalField(max_digits=12, decimal_places=2)
    description = models.CharField(max_length=255)
    posted_at = models.DateTimeField(db_index=True)
    deleted_at = models.DateTimeField(null=True, blank=True, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f"{self.entry_type} - {self.description}"


class SequenceCounter(models.Model):
    """Backs atomic invoice/payment number generation (see billing/sequences.py)."""

    prefix = models.CharField(max_length=16)
    period = models.CharField(max_length=8)
    last_value = models.PositiveIntegerField(default=0)

    class Meta:
        unique_together = ("prefix", "period")

    def __str__(self) -> str:
        return f"{self.prefix}-{self.period}: {self.last_value}"

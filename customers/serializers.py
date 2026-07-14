from rest_framework import serializers

from .models import Customer


class CustomerSerializer(serializers.ModelSerializer):
    customer_code = serializers.CharField(min_length=3, max_length=64)
    full_name = serializers.CharField(min_length=2, max_length=255)
    phone = serializers.CharField(min_length=6, max_length=32)
    address = serializers.CharField(min_length=5, max_length=255)
    city = serializers.CharField(min_length=2, max_length=128)

    class Meta:
        model = Customer
        fields = (
            "id",
            "customer_code",
            "full_name",
            "phone",
            "email",
            "address",
            "city",
            "zone",
            "status",
            "national_id",
            "notes",
            "created_at",
            "updated_at",
        )

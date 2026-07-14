from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED

from accounts.views import AdminAPIView
from aaa.exceptions import AppError
from common.casing import normalize_keys

from .models import Customer
from .serializers import CustomerSerializer


class CustomerListCreateView(AdminAPIView):
    def get(self, request):
        customers = Customer.objects.all().order_by("-created_at")
        return Response(CustomerSerializer(customers, many=True).data)

    def post(self, request):
        serializer = CustomerSerializer(data=normalize_keys(request.data))
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=HTTP_201_CREATED)


class CustomerDetailView(AdminAPIView):
    def get(self, request, customer_id):
        customer = Customer.objects.filter(id=customer_id).first()
        if customer is None:
            raise AppError("Customer not found", 404)
        return Response(CustomerSerializer(customer).data)

    def patch(self, request, customer_id):
        customer = Customer.objects.filter(id=customer_id).first()
        if customer is None:
            raise AppError("Customer not found", 404)
        serializer = CustomerSerializer(
            customer, data=normalize_keys(request.data), partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

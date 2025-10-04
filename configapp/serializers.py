from rest_framework import serializers
from .models import Employee, Client

class EmployeeStatisticsSerializer(serializers.Serializer):
    employee_id = serializers.IntegerField()
    full_name = serializers.CharField()
    unique_clients = serializers.IntegerField()
    total_products = serializers.IntegerField()
    total_sales = serializers.DecimalField(max_digits=12, decimal_places=2)

class ClientStatisticsSerializer(serializers.Serializer):
    client_id = serializers.IntegerField()
    full_name = serializers.CharField()
    total_products = serializers.IntegerField()
    total_sales = serializers.DecimalField(max_digits=12, decimal_places=2)

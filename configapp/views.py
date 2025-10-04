from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Sum, F
from django.shortcuts import get_object_or_404
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .models import Employee, Client, Order, OrderItem
from .serializers import EmployeeStatisticsSerializer, ClientStatisticsSerializer

class EmployeeStatisticsDetailView(APIView):
    """
    GET /statistics/employee/{id}/?month=1&year=2023
    """

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                'month', openapi.IN_QUERY,
                description="Oy raqami (1–12 oralig‘ida)",
                type=openapi.TYPE_INTEGER,
                required=True
            ),
            openapi.Parameter(
                'year', openapi.IN_QUERY,
                description="Yil (masalan: 2023)",
                type=openapi.TYPE_INTEGER,
                required=True
            ),
        ],
        responses={200: EmployeeStatisticsSerializer}
    )
    def get(self, request, id):
        month = request.query_params.get('month')
        year = request.query_params.get('year')

        if not (month and year):
            return Response({"error": "month va year parametrlarini yuboring"}, status=400)

        employee = get_object_or_404(Employee, id=id)
        orders = Order.objects.filter(
            employee=employee,
            order_date__year=year,
            order_date__month=month
        )

        order_items = OrderItem.objects.filter(order__in=orders)
        total_products = order_items.aggregate(total=Sum('quantity'))['total'] or 0
        total_sales = order_items.aggregate(total=Sum(F('price') * F('quantity')))['total'] or 0
        unique_clients = orders.values('client').distinct().count()

        data = {
            'employee_id': employee.id,
            'full_name': employee.full_name,
            'unique_clients': unique_clients,
            'total_products': total_products,
            'total_sales': total_sales,
        }

        return Response(data, status=200)

class AllEmployeesStatisticsView(APIView):
    """
    GET /employee/statistics/?month=1&year=2023
    """

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                'month', openapi.IN_QUERY,
                description="Oy raqami (1–12 oralig‘ida)",
                type=openapi.TYPE_INTEGER,
                required=True
            ),
            openapi.Parameter(
                'year', openapi.IN_QUERY,
                description="Yil (masalan: 2023)",
                type=openapi.TYPE_INTEGER,
                required=True
            ),
        ],
        responses={200: EmployeeStatisticsSerializer(many=True)}
    )
    def get(self, request):
        month = request.query_params.get('month')
        year = request.query_params.get('year')

        if not (month and year):
            return Response({"error": "month va year parametrlarini yuboring"}, status=400)

        employees = Employee.objects.all()
        result = []

        for emp in employees:
            orders = Order.objects.filter(
                employee=emp,
                order_date__year=year,
                order_date__month=month
            )

            order_items = OrderItem.objects.filter(order__in=orders)
            total_products = order_items.aggregate(total=Sum('quantity'))['total'] or 0
            total_sales = order_items.aggregate(total=Sum(F('price') * F('quantity')))['total'] or 0
            unique_clients = orders.values('client').distinct().count()

            result.append({
                'employee_id': emp.id,
                'full_name': emp.full_name,
                'unique_clients': unique_clients,
                'total_products': total_products,
                'total_sales': total_sales,
            })

        return Response(result, status=200)

class ClientStatisticsDetailView(APIView):
    """
    GET /statistics/client/{id}/?month=1&year=2023
    """

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                'month', openapi.IN_QUERY,
                description="Oy raqami (1–12 oralig‘ida)",
                type=openapi.TYPE_INTEGER,
                required=True
            ),
            openapi.Parameter(
                'year', openapi.IN_QUERY,
                description="Yil (masalan: 2023)",
                type=openapi.TYPE_INTEGER,
                required=True
            ),
        ],
        responses={200: ClientStatisticsSerializer}
    )
    def get(self, request, id):
        month = request.query_params.get('month')
        year = request.query_params.get('year')

        if not (month and year):
            return Response({"error": "month va year parametrlarini yuboring"}, status=400)

        client = get_object_or_404(Client, id=id)
        orders = Order.objects.filter(
            client=client,
            order_date__year=year,
            order_date__month=month
        )
        order_items = OrderItem.objects.filter(order__in=orders)

        total_products = order_items.aggregate(total=Sum('quantity'))['total'] or 0
        total_sales = order_items.aggregate(total=Sum(F('price') * F('quantity')))['total'] or 0

        data = {
            'client_id': client.id,
            'full_name': client.full_name,
            'total_products': total_products,
            'total_sales': total_sales,
        }

        return Response(data, status=200)

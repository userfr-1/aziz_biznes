from django.urls import path
from .views import EmployeeStatisticsDetailView, AllEmployeesStatisticsView, ClientStatisticsDetailView

urlpatterns = [
    path('statistics/employee/<int:id>/', EmployeeStatisticsDetailView.as_view()),
    path('employee/statistics/', AllEmployeesStatisticsView.as_view()),
    path('statistics/client/<int:id>/', ClientStatisticsDetailView.as_view()),
]

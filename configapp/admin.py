from django.contrib import admin
from .models import *
admin.site.register(Employee)
admin.site.register(Client)
admin.site.register(Product)
admin.site.register(Order)
admin.site.register(OrderItem)


# Register your models here.

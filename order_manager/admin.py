from django.contrib import admin
from order_manager.models import *

# Register your models here.
_admin = admin.site
_admin.register(Order)
_admin.register(OrderItem)
_admin.register(OrderDeliveryAddressStatus)
_admin.register(OrderPaymentStatus)
_admin.register(OrderDocs)
_admin.register(OrderComment)

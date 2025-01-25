from django.urls import path, include

from .views import OrderManagerViewSet, ServiceProviderViewSet, OrderItemViewSet
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r"order-manager-vset", OrderManagerViewSet)
router.register(r"service-provider-vset", ServiceProviderViewSet)
router.register(r"order-items-vset", OrderItemViewSet)

urlpatterns = [
    path("", include(router.urls)),
]

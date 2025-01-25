from django.urls import path, include

from .views import MeasumentsUnitsViewSet
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r"measumentsunits-vset", MeasumentsUnitsViewSet)

urlpatterns = [
    path("", include(router.urls)),
]

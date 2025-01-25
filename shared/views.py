from rest_framework import viewsets

from shared.models import MeasumentsUnits
from rest_framework.permissions import IsAuthenticated

from shared.serializers import GetMeasumentsUnitsSerializer


class MeasumentsUnitsViewSet(viewsets.ModelViewSet):
    queryset = MeasumentsUnits.objects.all()
    serializer_class = GetMeasumentsUnitsSerializer
    permission_classes = [IsAuthenticated]

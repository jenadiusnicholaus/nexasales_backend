from rest_framework import serializers

from shared.models import Entity, MeasumentsUnits


class GetEntitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Entity
        fields = "__all__"


class CreateEntitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Entity
        fields = "__all__"


class UpdateEntitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Entity
        fields = "__all__"


class GetMeasumentsUnitsSerializer(serializers.ModelSerializer):
    class Meta:
        fields = "__all__"
        model = MeasumentsUnits

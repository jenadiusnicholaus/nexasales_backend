from rest_framework import serializers

from order_manager.models import (
    Order,
    OrderItem,
    OrderPaymentStatus,
    OrderServiceProvider,
    OrderDeliveryAddressStatus,
)
from shared.serializers import GetEntitySerializer, GetMeasumentsUnitsSerializer


class GetOrderServiceProviderSerializer(serializers.ModelSerializer):
    entity = GetEntitySerializer()

    class Meta:
        model = OrderServiceProvider
        fields = "__all__"


class CreateOrderServiceProviderSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderServiceProvider
        fields = "__all__"


class UpdateOrderServiceProviderSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderServiceProvider
        fields = "__all__"


class GetOrderSerializer(serializers.ModelSerializer):
    service_provider = GetOrderServiceProviderSerializer()

    class Meta:
        model = Order

        fields = "__all__"


class CreateOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = "__all__"

        extra_kwargs = {
            "order_number": {
                "read_only": True,
                "required": False,
            },
        }


class UpdateOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = "__all__"


class GetOrderItemSerializer(serializers.ModelSerializer):
    qty_measurement_unit = GetMeasumentsUnitsSerializer()

    class Meta:
        model = OrderItem
        fields = "__all__"


class CreateOrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = "__all__"


class UpdateOrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = "__all__"


class OrderDeliveryAddressStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderDeliveryAddressStatus
        fields = "__all__"


class CreateOrderDeliveryAddressStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderDeliveryAddressStatus
        fields = "__all__"


class UpdateOrderDeliveryAddressStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderDeliveryAddressStatus
        fields = "__all__"


class GetOrderPaymentStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderPaymentStatus
        fields = "__all__"


class CreateOrderPaymentStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderPaymentStatus
        fields = "__all__"


class UpdateOrderPaymentStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderPaymentStatus
        fields = "__all__"

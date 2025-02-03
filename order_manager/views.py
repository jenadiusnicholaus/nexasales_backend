from rest_framework import viewsets

from order_manager.models import Order, OrderItem, OrderServiceProvider
from order_manager.serializers import (
    CreateOrderItemSerializer,
    CreateOrderPaymentStatusSerializer,
    CreateOrderSerializer,
    CreateOrderServiceProviderSerializer,
    GetOrderItemSerializer,
    GetOrderSerializer,
    GetOrderServiceProviderSerializer,
    UpdateOrderItemSerializer,
)
from rest_framework.permissions import IsAuthenticated

# from shared.permissions import IsOwnerOrReadOnly
from rest_framework.response import Response

from rest_framework import status
from shared.serializers import CreateEntitySerializer
from utils.paginators import CustomPageNumberPagination

from django.db import transaction


# Create your views here.
class OrderManagerViewSet(viewsets.ModelViewSet):
    serializer_class = GetOrderSerializer
    queryset = Order.objects.all()
    pagination_class = CustomPageNumberPagination

    def get_queryset(self):
        queryset = self.queryset.filter(user=self.request.user)
        return queryset

    def list(self, request, *args, **kwargs):
        # if (
        #     request.query_params.get("category", None) == "all"
        #     or request.query_params.get("category", None) is None
        #     or request.query_params.get("category", None) == ""
        # ):
        #     queryset = self.filter_queryset(self.get_queryset()).order_by("-created_at")
        # else:

        #     queryset = self.filter_queryset(
        #         self.get_queryset()
        #         .filter(category=request.query_params.get("category", None))
        #         .order_by("-created_at")
        #     )
        queryset = self.filter_queryset(self.get_queryset()).order_by("-created_at")

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(
            queryset, many=True, context={"request": request}
        )
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):

        order_data = {
            "user": request.user.id,
            "name": request.data.get("name"),
            "service_provider": request.data.get("service_provider_uuid"),
            "order_date": request.data.get("order_date"),
        }

        order_items = request.data.get("order_items")

        with transaction.atomic():
            order_serializer = CreateOrderSerializer(data=order_data)
            if not order_serializer.is_valid():
                return Response(
                    order_serializer.errors, status=status.HTTP_400_BAD_REQUEST
                )

            order = order_serializer.save()

            for item in order_items:
                order_item_data = {
                    "order": order.uuid,
                    "item_name": item.get("item_name"),
                    "qty": item.get("qty"),
                    "unit_price": item.get("unit_price"),
                    "qty_description": item.get("qty_description"),
                    "qty_measurement_unit": item.get("qty_measurement_unit_uuid"),
                }
                order_item_serializer = CreateOrderItemSerializer(data=order_item_data)
                if not order_item_serializer.is_valid():
                    return Response(
                        order_item_serializer.errors,
                        status=status.HTTP_400_BAD_REQUEST,
                    )
                order_item = order_item_serializer.save()
                order_payment_status_data = {
                    "order_item": None,
                    "status": item.get("status"),
                }
                order_payment_status_data["order_item"] = order_item.uuid
                order_payment_status_serializer = CreateOrderPaymentStatusSerializer(
                    data=order_payment_status_data
                )
                if not order_payment_status_serializer.is_valid():
                    return Response(
                        order_payment_status_serializer.errors,
                        status=status.HTTP_400_BAD_REQUEST,
                    )
                order_payment_status = order_payment_status_serializer.save()

            serializer = self.get_serializer(order)
            return Response(
                {
                    "message": "Order created successfully",
                },
                status=status.HTTP_201_CREATED,
            )


class ServiceProviderViewSet(viewsets.ModelViewSet):
    serializer_class = GetOrderServiceProviderSerializer
    queryset = OrderServiceProvider.objects.all()

    def list(self, request, *args, **kwargs):
        queryset = (
            self.filter_queryset(self.get_queryset())
            .filter(user=self.request.user)
            .order_by("-created_at")
        )

        serilazer = self.get_serializer(queryset, many=True)

        return Response(serilazer.data, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):

        entity_data = {
            "full_name": request.data.get("full_name"),
            "short_name": request.data.get("short_name"),
        }
        # CreateEntitySerializer

        order_service_provider_data = {"user": request.user.id, "entity": None}

        # CreateOrderServiceProviderSerializer

        with transaction.atomic():
            entity_serializer = CreateEntitySerializer(data=entity_data)

            if not entity_serializer.is_valid():
                return Response(
                    entity_serializer.errors,
                    status=status.HTTP_400_BAD_REQUEST,
                )

            entity = entity_serializer.save()

            order_service_provider_data["entity"] = entity.uuid

            order_service_provider_serializer = CreateOrderServiceProviderSerializer(
                data=order_service_provider_data
            )
            if not order_service_provider_serializer.is_valid():
                # delete the parent if child gone wrong
                entity.delete()
                return Response(
                    order_service_provider_serializer.errors,
                    status=status.HTTP_400_BAD_REQUEST,
                )

            order_service_provider = order_service_provider_serializer.save()
            serializer = self.get_serializer(order_service_provider)
            return Response(serializer.data, status=status.HTTP_201_CREATED)


class OrderItemViewSet(viewsets.ModelViewSet):
    serializer_class = GetOrderItemSerializer
    queryset = OrderItem.objects.all()

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset()).filter(
            order__user=self.request.user
        )
        order_uuid = self.request.query_params.get("order_uuid")
        if order_uuid:
            queryset = queryset.filter(order__uuid=order_uuid)
        sz = self.get_serializer(queryset, many=True)
        return Response(sz.data, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        item_data = {
            "order": request.data.get("order_uuid"),
            "item_name": request.data.get("item_name"),
            "qty": request.data.get("qty"),
            "unit_price": request.data.get("unit_price"),
            "qty_description": request.data.get("qty_description"),
            "qty_measurement_unit": request.data.get("qty_measurement_unit_uuid"),
        }
        order_item_serializer = CreateOrderItemSerializer(data=item_data)
        if not order_item_serializer.is_valid():
            return Response(
                order_item_serializer.errors, status=status.HTTP_400_BAD_REQUEST
            )

        order_item = order_item_serializer.save()

        order_payment_status_data = {
            "order_item": order_item.uuid,
            "status": request.data.get("status"),
        }

        order_payment_status_serializer = CreateOrderPaymentStatusSerializer(
            data=order_payment_status_data
        )
        if not order_payment_status_serializer.is_valid():
            order_item.delete()
            return Response(
                order_payment_status_serializer.errors,
                status=status.HTTP_400_BAD_REQUEST,
            )

        order_payment_status = order_payment_status_serializer.save()
        queryset = self.filter_queryset(self.get_queryset()).filter(
            order__uuid=order_uuid, order__user=self.request.user
        )

        sz = self.get_serializer(queryset, many=True)
        return Response(sz.data, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        item_data = {
            "order": request.data.get("order_uuid"),
            "item_name": request.data.get("item_name"),
            "qty": request.data.get("qty"),
            "unit_price": request.data.get("unit_price"),
            "qty_description": request.data.get("qty_description"),
            "qty_measurement_unit": request.data.get("qty_measurement_unit_uuid"),
        }
        order_item_serializer = CreateOrderItemSerializer(data=item_data)
        if not order_item_serializer.is_valid():
            return Response(
                order_item_serializer.errors, status=status.HTTP_400_BAD_REQUEST
            )

        order_item = order_item_serializer.save()

        order_payment_status_data = {
            "order_item": order_item.uuid,
            "status": request.data.get("status"),
        }

        order_payment_status_serializer = CreateOrderPaymentStatusSerializer(
            data=order_payment_status_data
        )
        if not order_payment_status_serializer.is_valid():
            order_item.delete()
            return Response(
                order_payment_status_serializer.errors,
                status=status.HTTP_400_BAD_REQUEST,
            )

        order_payment_status = order_payment_status_serializer.save()

        serializer = self.get_serializer(order_item)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def put(self, request, *args, **kwargs):
        item_uuid = self.request.query_params.get("item_uuid")
        order_uuid = self.request.query_params.get("order_uuid")
        order_item = OrderItem.objects.get(uuid=item_uuid)
        item_data = {
            "item_name": request.data.get("item_name", order_item.item_name),
            "qty": request.data.get("qty", order_item.qty),
            "unit_price": request.data.get("unit_price", order_item.unit_price),
            "qty_description": request.data.get(
                "qty_description", order_item.qty_description
            ),
            "qty_measurement_unit": request.data.get(
                "qty_measurement_unit_uuid",
                (
                    order_item.qty_measurement_unit.uuid
                    if order_item.qty_measurement_unit is not None
                    else None
                ),
            ),
        }
        order_item_serializer = UpdateOrderItemSerializer(
            order_item, data=item_data, partial=True
        )
        if not order_item_serializer.is_valid():
            return Response(
                order_item_serializer.errors, status=status.HTTP_400_BAD_REQUEST
            )

        order_item = order_item_serializer.save()

        order_payment_status_data = {
            "order_item": order_item.uuid,
            "status": request.data.get("status"),
        }

        order_payment_status_serializer = CreateOrderPaymentStatusSerializer(
            data=order_payment_status_data
        )
        if not order_payment_status_serializer.is_valid():
            return Response(
                order_payment_status_serializer.errors,
                status=status.HTTP_400_BAD_REQUEST,
            )

        order_payment_status = order_payment_status_serializer.save()

        serializer = self.get_serializer(order_item)
        return Response(serializer.data, status=status.HTTP_200_OK)

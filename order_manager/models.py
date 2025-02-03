from django.db import models
from django.contrib.auth.models import User

from shared.models import BaseModel, Entity, MeasumentsUnits
from utils.upload_handers import document_upload_to
import random
import string


class OrderServiceProvider(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    entity = models.ForeignKey(Entity, on_delete=models.CASCADE)

    class Meta:
        db_table = "order_water"
        verbose_name_plural = "order water"


class Order(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # supplier = models.ForeignKey(Entity, on_delete=models.CASCADE)
    service_provider = models.ForeignKey(
        OrderServiceProvider, on_delete=models.SET_NULL, null=True
    )
    order_number = models.CharField(max_length=255, null=True, blank=True)
    name = models.CharField(max_length=255, null=True, blank=True)
    order_date = models.DateField()
    to_be_billed = models.BooleanField(default=False)

    class Meta:
        unique_together = ("service_provider", "order_number")
        verbose_name_plural = "orders"
        db_table = "order"

    def __str__(self):
        return self.order_number

    def generate_order_number(self):
        # start with "NEXA"
        prefix = "NEXA"
        # generate random 5 digit number
        random_number = "".join(
            random.choices(string.digits, k=5)
        )  # random.randint(10000, 99999)
        # combine prefix and random number
        order_number = f"{prefix}-{random_number}"
        return order_number

    def save(self, *args, **kwargs):
        if not self.order_number:
            self.order_number = self.generate_order_number()
        super().save(*args, **kwargs)


class OrderItem(BaseModel):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    item_name = models.CharField(max_length=255)
    qty = models.IntegerField()
    qty_measurement_unit = models.ForeignKey(
        MeasumentsUnits, on_delete=models.SET_NULL, null=True
    )
    qty_description = models.CharField(max_length=255, null=True, blank=True)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        db_table = "order_item"


class OrderDeliveryAddress(BaseModel):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    state = models.CharField(max_length=255)
    zip_code = models.CharField(max_length=255)


class OrderBillingAddress(BaseModel):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    state = models.CharField(max_length=255)
    zip_code = models.CharField(max_length=255)

    class Meta:
        db_table = "order_billing_address"
        verbose_name_plural = "order billing addresses"


class OrderDelveryDetails(BaseModel):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    delivery_date = models.DateField()
    delivery_time = models.TimeField()
    delivery_instructions = models.TextField(null=True, blank=True)

    class Meta:
        db_table = "order_delivery_details"
        verbose_name_plural = "order delivery details"


class OrderDeliveryAddressStatus(BaseModel):
    STATUS = (
        ("draft", "Draft"),
        ("sent", "Sent"),
        ("received", "Received"),
        ("cancelled", "Cancelled"),
    )
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    status = models.CharField(max_length=255, choices=STATUS)
    status_date = models.DateField()

    class Meta:
        db_table = "order_status"
        verbose_name_plural = "order statuses"


class OderPayment(BaseModel):
    PAYEMNT_METHOD = (
        ("cash", "Cash"),
        ("check", "Check"),
        ("credit_card", "Credit Card"),
    )

    # order = models.ForeignKey(Order, on_delete=models.CASCADE)
    order_item = models.ForeignKey(OrderItem, on_delete=models.CASCADE, null=True)
    payment_date = models.DateField()
    payment_amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=255)

    class Meta:
        db_table = "order_payment"
        verbose_name_plural = "order payments"


class OrderPaymentStatus(BaseModel):
    STATUS = (
        ("PAID", "Paid"),
        ("UNPAID", "Unpaid"),
        ("PARTIALLY_PAID", "Partially Paid"),
    )
    # order = models.ForeignKey(Order, on_delete=models.CASCADE)
    order_item = models.ForeignKey(OrderItem, on_delete=models.CASCADE, null=True)

    status = models.CharField(max_length=255, choices=STATUS)

    class Meta:
        db_table = "order_payment_status"
        verbose_name_plural = "order payment statuses"


class OrderDocs(BaseModel):
    doc_type = models.CharField(max_length=255)
    doc = models.FileField(
        upload_to=document_upload_to,
    )

    class Meta:
        db_table = "order_docs"
        verbose_name_plural = "order orders "


class OrderComment(BaseModel):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    comment = models.TextField()

    class Meta:
        db_table = "order_comment"
        verbose_name_plural = "order comments"

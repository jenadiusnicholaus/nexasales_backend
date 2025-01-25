import uuid
from django.db import models


class BaseModel(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class MeasumentsUnits(BaseModel):
    name = models.CharField(max_length=255)
    symbol = models.CharField(max_length=255)

    class Meta:
        verbose_name_plural = "measuments units"
        db_table = "measuments_units"


# order waiter
class Entity(BaseModel):
    full_name = models.CharField(max_length=255)
    short_name = models.CharField(max_length=255)

    class Meta:
        verbose_name_plural = "entities"
        db_table = "entity"


class Contact(BaseModel):
    entity = models.ForeignKey(Entity, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=20)
    email = models.EmailField(max_length=255)

    class Meta:
        unique_together = ("entity", "phone_number", "email")
        verbose_name_plural = "contacts"
        db_table = "contact"

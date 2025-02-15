# Generated by Django 5.1.5 on 2025-01-25 14:40

import django.db.models.deletion
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order_manager', '0006_orderitem_qty_description'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='OrderStatus',
            new_name='OrderDeliveryAddressStatus',
        ),
        migrations.AddField(
            model_name='order',
            name='to_be_billed',
            field=models.BooleanField(default=False),
        ),
        migrations.CreateModel(
            name='OrderBillingAddress',
            fields=[
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('address', models.CharField(max_length=255)),
                ('city', models.CharField(max_length=255)),
                ('state', models.CharField(max_length=255)),
                ('zip_code', models.CharField(max_length=255)),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='order_manager.order')),
            ],
            options={
                'verbose_name_plural': 'order billing addresses',
                'db_table': 'order_billing_address',
            },
        ),
        migrations.CreateModel(
            name='OrderDeliveryAddress',
            fields=[
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('address', models.CharField(max_length=255)),
                ('city', models.CharField(max_length=255)),
                ('state', models.CharField(max_length=255)),
                ('zip_code', models.CharField(max_length=255)),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='order_manager.order')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='OrderDelveryDetails',
            fields=[
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('delivery_date', models.DateField()),
                ('delivery_time', models.TimeField()),
                ('delivery_instructions', models.TextField(blank=True, null=True)),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='order_manager.order')),
            ],
            options={
                'verbose_name_plural': 'order delivery details',
                'db_table': 'order_delivery_details',
            },
        ),
    ]

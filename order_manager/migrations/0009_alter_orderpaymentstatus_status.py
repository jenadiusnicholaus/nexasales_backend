# Generated by Django 5.1.5 on 2025-01-25 14:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order_manager', '0008_remove_orderpaymentstatus_payment_amount_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderpaymentstatus',
            name='status',
            field=models.CharField(choices=[('PAID', 'Paid'), ('UNPAID', 'Unpaid'), ('PARTIALLY_PAID', 'Partially Paid')], max_length=255),
        ),
    ]

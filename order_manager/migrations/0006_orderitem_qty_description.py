# Generated by Django 5.1.5 on 2025-01-25 14:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order_manager', '0005_remove_order_to_be_shipped'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderitem',
            name='qty_description',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]

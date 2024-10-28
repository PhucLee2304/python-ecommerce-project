# Generated by Django 5.1 on 2024-10-25 07:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_order_paymentdate'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='paymentMethod',
            field=models.CharField(choices=[('None', 'None'), ('Bank Transfer', 'Bank Transfer'), ('Cash on Delivery', 'Cash on Delivery')], default='None', max_length=20),
        ),
    ]
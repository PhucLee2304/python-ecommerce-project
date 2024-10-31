# Generated by Django 5.1 on 2024-10-31 09:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_alter_cartitem_quantity'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='orderStatus',
            field=models.CharField(choices=[('Pending', 'Pending'), ('Shipping', 'Shipping'), ('Delivered', 'Delivered'), ('Completed', 'Completed'), ('Cancelled', 'Cancelled')], default='Pending', max_length=10),
        ),
    ]

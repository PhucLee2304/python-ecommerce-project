# Generated by Django 5.1 on 2024-11-13 03:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0013_alter_review_order'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='orderStatus',
            field=models.CharField(choices=[('Pending', 'Pending'), ('Shipping', 'Shipping'), ('Completed', 'Completed'), ('Cancelled', 'Cancelled')], default='Pending', max_length=10),
        ),
    ]

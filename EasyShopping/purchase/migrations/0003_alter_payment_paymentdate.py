# Generated by Django 5.1.1 on 2024-10-21 02:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('purchase', '0002_alter_payment_paymentdate'),
    ]

    operations = [
        migrations.AlterField(
            model_name='payment',
            name='paymentDate',
            field=models.CharField(default='2024-10-21 09:24:01', max_length=19),
        ),
    ]

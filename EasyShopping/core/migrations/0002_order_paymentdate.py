# Generated by Django 5.1 on 2024-10-24 08:36

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='paymentDate',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]

# Generated by Django 5.1.1 on 2024-11-12 03:43

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0012_alter_review_order'),
    ]

    operations = [
        migrations.AlterField(
            model_name='review',
            name='order',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.order'),
        ),
    ]
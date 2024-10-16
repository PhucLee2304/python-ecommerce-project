# Generated by Django 5.1 on 2024-10-11 08:55

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('phone', models.CharField(blank=True, max_length=15, null=True)),
                ('address', models.CharField(blank=True, max_length=255, null=True)),
                ('gender', models.CharField(blank=True, choices=[('Male', 'Male'), ('Female', 'Female')], default='Male', max_length=10, null=True)),
                ('dateOfBirth', models.DateField(blank=True, default='2000-01-01', max_length=10, null=True)),
                ('userImage', models.ImageField(blank=True, default='static/images/userImageDefault.png', null=True, upload_to='customers/')),
            ],
            options={
                'db_table': 'customer',
            },
        ),
    ]

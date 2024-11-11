# Generated by Django 5.1.1 on 2024-11-11 00:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0008_alter_order_orderstatus'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='categoryImage',
            field=models.ImageField(default='\\categories\\category_image.jfif', upload_to='categories/'),
        ),
        migrations.AddField(
            model_name='product',
            name='shortDescription',
            field=models.CharField(default='this is short description', max_length=255),
        ),
        migrations.AlterField(
            model_name='order',
            name='orderStatus',
            field=models.CharField(choices=[('Pending', 'Pending'), ('Shipping', 'Shipping'), ('Delivered', 'Delivered'), ('Completed', 'Completed'), ('Cancelled', 'Cancelled'), ('Processing', 'Processing')], default='Processing', max_length=10),
        ),
    ]

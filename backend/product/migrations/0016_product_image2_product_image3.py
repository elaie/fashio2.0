# Generated by Django 4.1.6 on 2023-02-17 08:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0015_rename_produce_from_product_product_from'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='image2',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
        migrations.AddField(
            model_name='product',
            name='image3',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
    ]

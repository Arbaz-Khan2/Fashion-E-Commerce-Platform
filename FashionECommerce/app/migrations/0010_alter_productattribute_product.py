# Generated by Django 5.0 on 2023-12-11 14:24

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0009_alter_productattribute_product'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productattribute',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.product'),
        ),
    ]

# Generated by Django 4.0.5 on 2022-06-21 11:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0012_ordermodel_quantity'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='quantity',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
    ]

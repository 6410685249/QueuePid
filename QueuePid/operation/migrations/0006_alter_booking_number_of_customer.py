# Generated by Django 4.2.6 on 2023-11-17 18:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('operation', '0005_alter_operation_number_queue'),
    ]

    operations = [
        migrations.AlterField(
            model_name='booking',
            name='number_of_customer',
            field=models.IntegerField(null=True),
        ),
    ]

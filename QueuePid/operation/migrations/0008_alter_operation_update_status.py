# Generated by Django 4.2.5 on 2023-11-17 19:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('operation', '0007_alter_operation_number_of_customer'),
    ]

    operations = [
        migrations.AlterField(
            model_name='operation',
            name='update_status',
            field=models.BooleanField(default=False),
        ),
    ]

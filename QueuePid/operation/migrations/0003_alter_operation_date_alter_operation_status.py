# Generated by Django 4.2.5 on 2023-11-17 10:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('operation', '0002_alter_operation_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='operation',
            name='date',
            field=models.DateTimeField(null=True),
        ),
        migrations.AlterField(
            model_name='operation',
            name='status',
            field=models.IntegerField(default=-1),
        ),
    ]

# Generated by Django 4.2.6 on 2023-11-21 17:51

from django.db import migrations
import location_field.models.plain


class Migration(migrations.Migration):

    dependencies = [
        ('customers', '0006_alter_restaurant_location'),
    ]

    operations = [
        migrations.AlterField(
            model_name='restaurant',
            name='location',
            field=location_field.models.plain.PlainLocationField(default=None, max_length=63, null=True),
        ),
    ]

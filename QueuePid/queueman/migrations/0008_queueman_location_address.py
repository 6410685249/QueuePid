# Generated by Django 4.2.6 on 2023-11-26 11:45

from django.db import migrations
import location_field.models.plain


class Migration(migrations.Migration):

    dependencies = [
        ('queueman', '0007_alter_queueman_upload'),
    ]

    operations = [
        migrations.AddField(
            model_name='queueman',
            name='location_address',
            field=location_field.models.plain.PlainLocationField(blank=True, default=None, max_length=63, null=True),
        ),
    ]

# Generated by Django 4.2.6 on 2023-11-16 19:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0007_alter_user_info_book'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user_info',
            name='book',
            field=models.CharField(blank=True, default=None, max_length=30, null=True),
        ),
    ]

# Generated by Django 4.2.6 on 2023-11-18 11:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0008_alter_user_info_book'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user_info',
            name='credit',
            field=models.IntegerField(default=0),
        ),
    ]

# Generated by Django 4.2.6 on 2023-11-24 20:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0010_user_info_upload'),
    ]

    operations = [
        migrations.AddField(
            model_name='user_info',
            name='credit_topUp',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='user_info',
            name='message_from_admin',
            field=models.CharField(default='', max_length=100),
        ),
    ]
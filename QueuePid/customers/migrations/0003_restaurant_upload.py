# Generated by Django 4.2.7 on 2023-11-09 15:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customers', '0002_alter_historically_date_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='restaurant',
            name='upload',
            field=models.ImageField(null=True, upload_to='uploads/'),
        ),
    ]

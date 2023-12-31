# Generated by Django 4.2.6 on 2023-11-06 17:21

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='User_info',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('telephone', models.CharField(max_length=10)),
                ('password', models.CharField(max_length=20)),
                ('name', models.CharField(max_length=30)),
                ('surname', models.CharField(max_length=30)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('type', models.CharField(default='customer', max_length=10)),
                ('credit', models.PositiveIntegerField(default='customer')),
                ('username', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]

# Generated by Django 5.1 on 2024-09-01 17:45

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cast_member_app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='castmembermodel',
            name='created_at',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
# Generated by Django 5.1 on 2024-08-30 09:31

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CastMemberModel',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
                ('type', models.CharField(choices=[('ACTOR', 'ACTOR'), ('DIRECTOR', 'DIRECTOR')], max_length=64)),
            ],
            options={
                'db_table': 'cast_member',
            },
        ),
    ]
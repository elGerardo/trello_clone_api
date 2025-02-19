# Generated by Django 5.0.3 on 2024-04-01 02:13

import django.db.models.deletion
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('priority', '0001_initial'),
        ('steps', '0001_initial'),
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tasks',
            fields=[
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('deleted_at', models.DateTimeField(default=None, null=True)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('title', models.CharField(default=None, max_length=255, null=True)),
                ('description', models.TextField(default=None, null=True)),
                ('secuence', models.IntegerField()),
                ('is_finished', models.BooleanField(editable=True, default=False)),
                ('priority', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='priority.priority')),
                ('step', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='steps.steps')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.user')),
            ],
            options={
                'db_table': 'tasks',
            },
        ),
    ]

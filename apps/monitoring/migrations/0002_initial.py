# Generated by Django 5.0.2 on 2024-02-26 15:20

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('monitoring', '0001_initial'),
        ('service', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='uptimerecord',
            name='service',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='service.service'),
        ),
    ]

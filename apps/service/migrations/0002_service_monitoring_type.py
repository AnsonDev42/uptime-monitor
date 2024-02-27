# Generated by Django 5.0.2 on 2024-02-26 23:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('service', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='service',
            name='monitoring_type',
            field=models.CharField(choices=[('http', 'HTTP'), ('ping', 'PING')], default='http', max_length=50),
        ),
    ]
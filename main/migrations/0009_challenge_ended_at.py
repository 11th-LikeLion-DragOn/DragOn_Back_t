# Generated by Django 3.2 on 2024-01-06 10:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0008_auto_20240106_1951'),
    ]

    operations = [
        migrations.AddField(
            model_name='challenge',
            name='ended_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
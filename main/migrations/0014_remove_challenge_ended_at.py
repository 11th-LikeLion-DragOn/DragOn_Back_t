# Generated by Django 3.2 on 2024-01-06 11:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0013_challenge_ended_at'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='challenge',
            name='ended_at',
        ),
    ]

# Generated by Django 3.2 on 2024-01-13 08:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0028_ball_last_updated'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ball',
            name='count',
            field=models.IntegerField(default=0),
        ),
    ]

# Generated by Django 3.2 on 2023-12-28 16:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_user_balls'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='profile',
            field=models.CharField(choices=[('red', 'red'), ('yellow', 'yellow'), ('gray', 'gray'), ('pink', 'pink'), ('white', 'white')], max_length=10, null=True),
        ),
    ]

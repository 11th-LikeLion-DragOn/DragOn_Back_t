# Generated by Django 3.2 on 2024-01-05 13:03

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('main', '0005_auto_20240104_1411'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='challenge',
            name='time',
        ),
        migrations.AddField(
            model_name='ball',
            name='challenge',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='main.challenge'),
        ),
        migrations.AddField(
            model_name='ball',
            name='is_use',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='ball',
            name='time',
            field=models.IntegerField(default=1),
        ),
        migrations.AlterField(
            model_name='achieve',
            name='goal',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='achieves', to='main.goals'),
        ),
        migrations.AlterField(
            model_name='ball',
            name='count',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterUniqueTogether(
            name='ball',
            unique_together={('user', 'challenge')},
        ),
        migrations.CreateModel(
            name='Reaction',
            fields=[
                ('reaction_id', models.AutoField(primary_key=True, serialize=False)),
                ('type', models.IntegerField(choices=[(1, 'Good'), (2, 'Question'), (3, 'Fighting'), (4, 'Fire'), (5, 'Mark'), (6, 'Heart')])),
                ('challenge', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.challenge')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
# Generated by Django 4.1 on 2022-08-06 14:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Waiter', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='table',
            name='availeble',
        ),
        migrations.AddField(
            model_name='table',
            name='available',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='table',
            name='occupied',
            field=models.BooleanField(default=True),
        ),
    ]

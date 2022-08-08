# Generated by Django 4.1 on 2022-08-08 20:14

import ckeditor.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Waiter', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderkitchen',
            name='dishes',
            field=ckeditor.fields.RichTextField(),
        ),
        migrations.AlterField(
            model_name='orderkitchen',
            name='status',
            field=models.CharField(choices=[('new', 'new'), ('in progress', 'in progress'), ('done', 'done')], default='new', max_length=256),
        ),
    ]

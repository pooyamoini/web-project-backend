# Generated by Django 3.0.2 on 2020-02-03 14:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0013_auto_20200203_1417'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='number',
            name='number',
        ),
    ]

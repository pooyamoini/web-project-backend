# Generated by Django 3.0.2 on 2020-01-28 15:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0011_logginbasic_token_gen_time'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='logginbasic',
            name='token_gen_time',
        ),
    ]

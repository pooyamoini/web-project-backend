# Generated by Django 3.0.2 on 2020-01-29 15:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0013_logginbasic_token_gen_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='logginbasic',
            name='token',
            field=models.CharField(max_length=110),
        ),
    ]

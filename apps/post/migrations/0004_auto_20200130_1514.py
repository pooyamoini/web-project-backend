# Generated by Django 3.0.2 on 2020-01-30 15:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0003_auto_20200130_1422'),
    ]

    operations = [
        migrations.RenameField(
            model_name='post',
            old_name='id',
            new_name='id_post',
        ),
    ]
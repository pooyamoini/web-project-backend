# Generated by Django 3.0.2 on 2020-01-31 13:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('like', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='like',
            old_name='post_id',
            new_name='comment_id',
        ),
    ]

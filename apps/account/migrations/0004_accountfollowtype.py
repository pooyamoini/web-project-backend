# Generated by Django 3.0.2 on 2020-01-29 15:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0003_auto_20200126_1622'),
    ]

    operations = [
        migrations.CreateModel(
            name='AccountFollowType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('follower_id', models.CharField(default='', max_length=15)),
                ('followed_id', models.CharField(default='', max_length=15)),
            ],
        ),
    ]
# Generated by Django 3.0.2 on 2020-02-04 10:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('content', models.CharField(max_length=50000)),
                ('id_post', models.IntegerField(primary_key=True, serialize=False)),
                ('image', models.CharField(default='', max_length=100)),
                ('date_post', models.DateTimeField(auto_now=True)),
                ('account', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='account.AccountBasic')),
                ('ndislikes', models.ManyToManyField(related_name='ndislikes', to='account.AccountBasic')),
                ('nlikes', models.ManyToManyField(related_name='nlikes', to='account.AccountBasic')),
            ],
        ),
    ]

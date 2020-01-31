# Generated by Django 3.0.2 on 2020-01-30 21:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('account', '0014_auto_20200129_1510'),
        ('post', '0005_auto_20200130_2147'),
    ]

    operations = [
        migrations.CreateModel(
            name='AccountGeneric',
            fields=[
                ('account', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, primary_key=True, related_name='accounts', serialize=False, to='account.AccountBasic')),
                ('followers', models.ManyToManyField(related_name='followrs', to='account.AccountBasic')),
                ('followings', models.ManyToManyField(related_name='followings', to='account.AccountBasic')),
                ('posts', models.ManyToManyField(to='post.Post')),
            ],
        ),
    ]
# Generated by Django 3.0.2 on 2020-02-03 14:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0008_number'),
    ]

    operations = [
        migrations.AddField(
            model_name='number',
            name='name',
            field=models.CharField(default='n', max_length=100, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='number',
            name='number',
            field=models.IntegerField(default=0),
        ),
    ]

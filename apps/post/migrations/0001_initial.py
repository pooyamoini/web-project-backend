# Generated by Django 3.0.2 on 2020-01-30 14:05

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('nlikes', models.IntegerField()),
                ('ndislikes', models.IntegerField()),
                ('content', models.CharField(max_length=50000)),
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('image', models.ImageField(upload_to='statics.images')),
                ('dete_post', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]

# Generated by Django 2.0 on 2019-06-19 20:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('article', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='love_num',
            field=models.IntegerField(default=0, verbose_name='收藏量'),
        ),
    ]

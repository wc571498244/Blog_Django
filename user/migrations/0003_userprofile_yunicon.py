# Generated by Django 2.0 on 2019-06-19 16:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_remove_userprofile_mobile'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='yunIcon',
            field=models.CharField(default='', max_length=300),
        ),
    ]

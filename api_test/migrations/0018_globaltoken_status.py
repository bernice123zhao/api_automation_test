# Generated by Django 2.0.2 on 2020-08-17 11:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api_test', '0017_globaltoken_globalhost'),
    ]

    operations = [
        migrations.AddField(
            model_name='globaltoken',
            name='status',
            field=models.BooleanField(default=True, verbose_name='状态'),
        ),
    ]

# Generated by Django 2.0.2 on 2020-07-13 17:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api_test', '0003_globaltoken'),
    ]

    operations = [
        migrations.AlterField(
            model_name='globaltoken',
            name='value',
            field=models.CharField(max_length=1000, verbose_name='值'),
        ),
    ]

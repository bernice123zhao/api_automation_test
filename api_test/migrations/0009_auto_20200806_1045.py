# Generated by Django 2.0.2 on 2020-08-06 10:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api_test', '0008_auto_20200805_1439'),
    ]

    operations = [
        migrations.AlterField(
            model_name='automationtesttask',
            name='frequency',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='参数'),
        ),
    ]

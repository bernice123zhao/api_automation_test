# Generated by Django 2.0.2 on 2020-08-05 14:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api_test', '0007_automationcaseapi_exesequence'),
    ]

    operations = [
        migrations.AlterField(
            model_name='automationcaseapi',
            name='exeSequence',
            field=models.FloatField(blank=True, max_length=20, null=True, verbose_name='执行顺序'),
        ),
    ]

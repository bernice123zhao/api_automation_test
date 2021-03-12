# Generated by Django 2.0.2 on 2020-09-02 16:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api_test', '0023_auto_20200901_1034'),
    ]

    operations = [
        migrations.AddField(
            model_name='automationcaseapi',
            name='_type',
            field=models.CharField(blank=True, choices=[('Int', 'Int'), ('String', 'String'), ('Bool', 'Bool')], default='String', max_length=50, null=True, verbose_name='参数类型'),
        ),
    ]

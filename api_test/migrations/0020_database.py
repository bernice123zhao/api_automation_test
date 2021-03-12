# Generated by Django 2.0.2 on 2020-08-18 11:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api_test', '0019_auto_20200817_1437'),
    ]

    operations = [
        migrations.CreateModel(
            name='DataBase',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('host', models.CharField(choices=[('1', 'Mysql'), ('2', 'SQL Server')], max_length=50, verbose_name='host')),
                ('user', models.CharField(max_length=50, verbose_name='user')),
                ('passwd', models.CharField(max_length=50, verbose_name='passwd')),
                ('dataname', models.CharField(max_length=50, verbose_name='数据库名')),
                ('name', models.CharField(max_length=50, verbose_name='数据库名')),
            ],
            options={
                'verbose_name': '数据库信息',
                'verbose_name_plural': '数据库信息',
            },
        ),
    ]

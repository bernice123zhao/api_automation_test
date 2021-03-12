# Generated by Django 2.0.2 on 2020-07-13 16:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api_test', '0002_auto_20200510_1655'),
    ]

    operations = [
        migrations.CreateModel(
            name='GlobalToken',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('key', models.CharField(max_length=50, verbose_name='值')),
                ('value', models.CharField(max_length=500, verbose_name='值')),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api_test.Project', verbose_name='项目')),
            ],
        ),
    ]
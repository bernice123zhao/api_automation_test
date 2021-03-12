# Generated by Django 2.0.2 on 2020-08-17 14:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api_test', '0018_globaltoken_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='globalhost',
            name='LastUpdateTime',
            field=models.DateTimeField(auto_now=True, null=True, verbose_name='最近修改时间'),
        ),
        migrations.AddField(
            model_name='globalhost',
            name='key',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='头部key'),
        ),
        migrations.AddField(
            model_name='globalhost',
            name='password',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='获取token的密码'),
        ),
        migrations.AddField(
            model_name='globalhost',
            name='url',
            field=models.CharField(blank=True, max_length=500, null=True, verbose_name='登录地址'),
        ),
        migrations.AddField(
            model_name='globalhost',
            name='username',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='获取token的账号'),
        ),
        migrations.AddField(
            model_name='globalhost',
            name='value',
            field=models.CharField(blank=True, max_length=5000, null=True, verbose_name='头部value'),
        ),
    ]
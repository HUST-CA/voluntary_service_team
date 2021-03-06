# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-11-30 12:35
from __future__ import unicode_literals

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('service_activity', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ServiceObject',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=16, verbose_name='姓名')),
                ('tel', models.CharField(max_length=11, verbose_name='电话')),
                ('computer_model', models.CharField(blank=True, max_length=64, verbose_name='电脑品牌/型号')),
                ('problem', models.TextField(verbose_name='电脑故障')),
                ('send_time', models.DateTimeField(auto_now_add=True, verbose_name='送到时间')),
                ('flag', models.CharField(choices=[('完成', '完成'), ('修理中', '修理中'), ('已取回', '已取回'), ('遇到问题需反馈', '遇到问题需反馈')], max_length=64, verbose_name='修理状态')),
                ('trouble', models.TextField(blank=True, verbose_name='遇到的问题')),
                ('short_link', models.CharField(max_length=32, verbose_name='短链接')),
                ('serial_number', models.CharField(max_length=16, verbose_name='取货号')),
                ('service_activity', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='service_objects', to='service_activity.ServiceActivity', verbose_name='从属哪次活动')),
            ],
            options={
                'verbose_name': '服务对象',
                'verbose_name_plural': '服务对象',
            },
        ),
        migrations.CreateModel(
            name='SMS_Feedback',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(max_length=256, verbose_name='短信回复内容')),
                ('reply_time', models.DateTimeField(verbose_name='回复短信时间')),
                ('service_object',
                 models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sms_feedback',
                                   to='service_inform.ServiceObject', verbose_name='从属哪个服务对象')),
            ],
            options={
                'verbose_name': '短信回复',
                'verbose_name_plural': '短信回复',
            },
        ),
    ]

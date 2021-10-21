# Generated by Django 3.1 on 2021-09-24 08:23

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BaseTables',
            fields=[
                ('id', models.CharField(max_length=10, primary_key=True, serialize=False, verbose_name='序号')),
                ('creator', models.CharField(max_length=50, verbose_name='模式名')),
                ('table_name', models.CharField(max_length=100, verbose_name='下发表名')),
                ('ds_id', models.CharField(max_length=10, verbose_name='渠道名')),
                ('flag', models.BooleanField(verbose_name='是否生效')),
                ('chn_name', models.CharField(max_length=100, verbose_name='表中文名')),
                ('create_date', models.DateTimeField(verbose_name='创建日期')),
            ],
            options={
                'verbose_name': '数据下发基础表',
                'verbose_name_plural': '数据下发基础表',
            },
        ),
        migrations.CreateModel(
            name='DataRelation',
            fields=[
                ('id', models.BigIntegerField(primary_key=True, serialize=False, verbose_name='序号')),
                ('user_id', models.CharField(db_index=True, max_length=10, verbose_name='机构编号')),
                ('org_name', models.CharField(db_index=True, max_length=100, verbose_name='机构名称')),
                ('ds_id', models.CharField(max_length=10, verbose_name='渠道编号')),
                ('table_name', models.CharField(db_index=True, max_length=100, verbose_name='下发表名')),
                ('create_date', models.DateTimeField(null=True, verbose_name='创建日期')),
            ],
            options={
                'verbose_name': '数据下发关系',
                'verbose_name_plural': '数据下发关系',
                'ordering': ['user_id', 'ds_id'],
            },
        ),
        migrations.CreateModel(
            name='DataSub',
            fields=[
                ('id', models.BigIntegerField(primary_key=True, serialize=False, verbose_name='序号')),
                ('user_id', models.CharField(db_index=True, max_length=10, verbose_name='机构编号')),
                ('ds_id', models.CharField(max_length=10, verbose_name='渠道编号')),
                ('ds_type', models.IntegerField(verbose_name='类型')),
                ('t_id', models.CharField(max_length=50, verbose_name='数据表名')),
                ('seq', models.IntegerField(verbose_name='顺序号')),
                ('file_type', models.CharField(max_length=10, verbose_name='文件类型')),
                ('modified', models.CharField(max_length=150, verbose_name='导出限定')),
                ('h_sql', models.CharField(max_length=2000, verbose_name='导出语句')),
                ('h_where', models.CharField(max_length=500, verbose_name='查询条件')),
                ('c_user_id', models.CharField(max_length=10, verbose_name='村镇银行编号')),
                ('a_where', models.CharField(max_length=500, verbose_name='全量查询条件')),
                ('create_date', models.DateTimeField(verbose_name='创建日期')),
            ],
            options={
                'verbose_name': '数据下发任务',
                'verbose_name_plural': '数据下发任务',
            },
        ),
        migrations.CreateModel(
            name='DataUsers',
            fields=[
                ('user_id', models.CharField(max_length=10, primary_key=True, serialize=False, verbose_name='用户编号')),
                ('org_name', models.CharField(max_length=100, verbose_name='机构名称')),
                ('create_date', models.DateTimeField(verbose_name='接入时间')),
            ],
            options={
                'verbose_name': '数据下发用户表',
                'verbose_name_plural': '数据下发用户表',
            },
        ),
        migrations.CreateModel(
            name='TaskList',
            fields=[
                ('task_id', models.UUIDField(primary_key=True, serialize=False, verbose_name='任务编号')),
                ('user_id', models.CharField(default='admin', max_length=20, verbose_name='提交人')),
                ('user_name', models.CharField(default='', max_length=50, verbose_name='提交人姓名')),
                ('org_no', models.CharField(max_length=10, verbose_name='机构编号')),
                ('table_name', models.CharField(max_length=100, verbose_name='下发表名')),
                ('v_flag', models.BooleanField(verbose_name='有效标识')),
                ('remarks', models.CharField(blank=True, max_length=100, null=True, verbose_name='备注')),
                ('created_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('updated_time', models.DateTimeField(auto_now=True, verbose_name='上次修改时间')),
            ],
            options={
                'verbose_name': '任务清单',
                'verbose_name_plural': '任务清单',
            },
        ),
    ]
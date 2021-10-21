# Generated by Django 3.1 on 2021-09-27 02:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sjxf', '0002_tasklist_status'),
    ]

    operations = [
        migrations.CreateModel(
            name='Metrics',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('metric', models.CharField(max_length=50, verbose_name='指标名')),
                ('metric_chn_name', models.CharField(max_length=200, verbose_name='指标中文名')),
                ('period', models.IntegerField(verbose_name='')),
            ],
        ),
        migrations.AlterModelOptions(
            name='tasklist',
            options={'verbose_name': '下发任务清单', 'verbose_name_plural': '下发任务清单'},
        ),
        migrations.RemoveField(
            model_name='tasklist',
            name='v_flag',
        ),
        migrations.AlterField(
            model_name='tasklist',
            name='status',
            field=models.CharField(choices=[('0', '已提交'), ('1', '执行中'), ('2', '执行完成'), ('3', '执行失败')], max_length=1, verbose_name='执行状态'),
        ),
    ]

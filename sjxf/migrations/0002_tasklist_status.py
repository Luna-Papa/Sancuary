# Generated by Django 3.1 on 2021-09-24 17:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sjxf', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='tasklist',
            name='status',
            field=models.CharField(choices=[('0', '未执行'), ('1', '执行开始'), ('2', '执行完成'), ('3', '执行失败')], default='0', max_length=1, verbose_name='执行状态'),
            preserve_default=False,
        ),
    ]

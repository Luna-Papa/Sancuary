# Generated by Django 3.1 on 2021-09-27 09:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sjxf', '0004_tasklist_v_flag'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tasklist',
            name='task_id',
            field=models.CharField(max_length=256, primary_key=True, serialize=False, verbose_name='任务编号'),
        ),
    ]

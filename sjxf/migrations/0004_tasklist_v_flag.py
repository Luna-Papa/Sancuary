# Generated by Django 3.1 on 2021-09-27 09:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sjxf', '0003_auto_20210927_1007'),
    ]

    operations = [
        migrations.AddField(
            model_name='tasklist',
            name='v_flag',
            field=models.BooleanField(default=1, verbose_name='有效标识'),
            preserve_default=False,
        ),
    ]

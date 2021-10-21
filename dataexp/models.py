from django.db import models

# Create your models here.


class DBTypes(models.IntegerChoices):
    """数据库类型定义"""
    db2 = 1, 'DB2'
    orc = 2, 'Oracle'
    mysql = 3, 'Mysql'
    hive = 4, 'Hive'


class SystemInfo(models.Model):
    sys_name = models.CharField(verbose_name='系统英文简称', max_length=50)
    chn_name = models.CharField(verbose_name='中文名称', max_length=128)
    db_type = models.PositiveSmallIntegerField(verbose_name='数据库类型',
                                               default=DBTypes.db2, choices=DBTypes.choices)
    db_name = models.CharField(verbose_name='数据库名', max_length=128, unique=True)
    address = models.GenericIPAddressField(verbose_name='IP地址')
    port = models.CharField(verbose_name='端口', max_length=20)
    codepage = models.CharField(verbose_name='字符集', max_length=10)
    username = models.CharField(verbose_name='用户名', max_length=50)
    password = models.CharField(verbose_name='密码', max_length=50)
    val_flag = models.BooleanField(verbose_name='有效标识', default=True)
    created_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_time = models.DateTimeField(auto_now=True, verbose_name='上次修改时间')

    def __str__(self):
        return self.chn_name

    class Meta:
        verbose_name = '系统定义'
        verbose_name_plural = verbose_name
        ordering = ['sys_name']


class ExpTaskList(models.Model):
    task_no = models.UUIDField(verbose_name='任务编号', db_index=True)
    user_id = models.CharField(max_length=20, verbose_name='提交人', default='admin')
    username = models.CharField(verbose_name='提交人姓名', max_length=50)
    sys_name = models.CharField(verbose_name='系统名', max_length=50)
    table_name = models.CharField(verbose_name='数据表名', max_length=100)
    file_type = models.CharField(verbose_name='导出文件格式',
                                 choices=(('txt', 'txt'), ('ixf', 'ixf')), max_length=3)
    exp_method = models.CharField(verbose_name='导出方式',
                                  choices=(('exp', 'exp'), ('hpu', 'hpu')), max_length=10)
    code_page = models.CharField(verbose_name='编码格式', max_length=10,
                                 choices=(('1386', '1386'), ('1208', '1208')))
    delimiter = models.CharField(verbose_name='字符串定界符', max_length=10, null=True, blank=True,
                                 help_text='不指定则默认为"')
    separator = models.CharField(verbose_name='字符列定界符', max_length=10, null=True, blank=True,
                                 help_text='不指定则默认为，')
    work_date = models.CharField(verbose_name='数据日期', max_length=10)
    created_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_time = models.DateTimeField(auto_now=True, verbose_name='上次修改时间')

    def __str__(self):
        return self.task_no

    class Meta:
        verbose_name = '数据提取任务清单'
        verbose_name_plural = verbose_name
        ordering = ['task_no']

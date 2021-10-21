from django.db import models
from users.models import UserInfo
# Create your models here.


class StatusTypes(models.TextChoices):
    """任务状态类型定义"""
    status_submit = '0', '已提交'
    status_execute = '1', '执行中'
    status_success = '2', '执行完成'
    status_failed = '3', '执行失败'
    status_cancel = '4', '已取消'


class BaseTables(models.Model):
    """ 数据下发基础表定义"""
    id = models.CharField(verbose_name='序号', max_length=10, primary_key=True)
    creator = models.CharField(verbose_name='模式名', max_length=50)
    table_name = models.CharField(verbose_name='下发表名', max_length=100)
    ds_id = models.CharField(verbose_name='渠道名', max_length=10)
    flag = models.BooleanField(verbose_name='是否生效')
    chn_name = models.CharField(verbose_name='表中文名', max_length=100)
    create_date = models.DateTimeField(verbose_name='创建日期')

    class Meta:
        verbose_name = '数据下发基础表'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.table_name


class DataUsers(models.Model):
    """数据下发用户"""
    user_id = models.CharField(verbose_name='用户编号', max_length=10, primary_key=True)
    org_name = models.CharField(verbose_name='机构名称', max_length=100)
    create_date = models.DateTimeField(verbose_name='接入时间')
    # address = models.GenericIPAddressField(verbose_name='IP地址')
    # port = models.IntegerField(verbose_name='端口')
    # flag = models.BooleanField(verbose_name='激活标识')
    # user_no = models.CharField(verbose_name='用户编号', max_length=10, null=True)
    # pass_no = models.CharField(verbose_name='文件密码', max_length=10, null=True)

    class Meta:
        verbose_name = '数据下发用户表'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.user_id


class DataSub(models.Model):
    id = models.BigIntegerField(verbose_name='序号', primary_key=True)
    user_id = models.CharField(verbose_name='机构编号', max_length=10, db_index=True)
    ds_id = models.CharField(verbose_name='渠道编号', max_length=10)
    ds_type = models.IntegerField(verbose_name='类型')
    t_id = models.CharField(max_length=50, verbose_name='数据表名')
    seq = models.IntegerField(verbose_name='顺序号')
    file_type = models.CharField(max_length=10, verbose_name='文件类型')
    modified = models.CharField(verbose_name='导出限定', max_length=150)
    h_sql = models.CharField(verbose_name='导出语句', max_length=2000)
    h_where = models.CharField(verbose_name='查询条件', max_length=500)
    c_user_id = models.CharField(verbose_name='村镇银行编号', max_length=10)
    a_where = models.CharField(verbose_name='全量查询条件', max_length=500)
    create_date = models.DateTimeField(verbose_name='创建日期')

    class Meta:
        verbose_name = '数据下发任务'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.user_id


class DataRelation(models.Model):
    id = models.BigIntegerField(verbose_name='序号', primary_key=True)
    user_id = models.CharField(verbose_name='机构编号', max_length=10, db_index=True)
    org_name = models.CharField(verbose_name='机构名称', max_length=100, db_index=True)
    ds_id = models.CharField(verbose_name='渠道编号', max_length=10)
    table_name = models.CharField(verbose_name='下发表名', max_length=100, db_index=True)
    # c_user_id = models.CharField(verbose_name='村镇银行编号', max_length=10)
    create_date = models.DateTimeField(verbose_name='创建日期', null=True)

    class Meta:
        verbose_name = '数据下发关系'
        verbose_name_plural = verbose_name
        ordering = ['user_id', 'ds_id']

    def __str__(self):
        return self.user_id


class TaskList(models.Model):
    task_id = models.CharField(verbose_name='任务编号', max_length=255, primary_key=True)
    user_id = models.CharField(max_length=20, verbose_name='提交人', default='admin')
    user_name = models.CharField(verbose_name='提交人姓名', max_length=50, default='')
    org_no = models.CharField(verbose_name='机构编号', max_length=10)
    table_name = models.CharField(verbose_name='下发表名', max_length=100)
    remarks = models.CharField(verbose_name='备注', max_length=100, null=True, blank=True)
    status = models.CharField(verbose_name='任务状态', choices=StatusTypes.choices, max_length=1)
    # v_flag = models.BooleanField(verbose_name='有效标识')
    created_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_time = models.DateTimeField(auto_now=True, verbose_name='上次修改时间')
    celery_task_id = models.CharField(verbose_name='Celery任务号', max_length=255, null=True, blank=True)

    class Meta:
        verbose_name = '下发任务清单'
        verbose_name_plural = verbose_name

    def __str__(self):
        return str(self.task_id)

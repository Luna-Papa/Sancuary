from django.db import models


# Create your models here.


class PeriodTypes(models.TextChoices):
    """任务周期类型定义"""
    day = 'day', '天'
    week = 'week', '周'
    month = 'month', '月'
    year = 'year', '年'


class DatabaseTypes(models.TextChoices):
    """任务周期类型定义"""
    DB2 = 'DB2', 'DB2'
    MySql = 'MySql', 'MySql'
    Oracle = 'Oracle', 'Oracle'
    PostgreSQL = 'PostgreSQL', 'PostgreSQL'
    DaMeng = 'DaMeng', 'Dameng'


class Metrics(models.Model):
    """指标定义表"""
    metric = models.CharField(verbose_name='指标名', max_length=50)
    chn_name = models.CharField(verbose_name='指标中文名', max_length=200)
    period = models.CharField(verbose_name='指标统计周期', choices=PeriodTypes.choices,
                              default=PeriodTypes.month, max_length=10)
    describe = models.TextField(verbose_name='指标描述', null=True, blank=True)
    v_flag = models.BooleanField(verbose_name='有效标识', default=True)
    special_flag = models.BooleanField(verbose_name='特殊处理标识', default=False)  # 标识该指标由单独的函数来计算
    created_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_time = models.DateTimeField(auto_now=True, verbose_name='上次修改时间')

    class Meta:
        verbose_name = '统计指标定义'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.metric


class MetricsDetail(models.Model):
    """指标运行结果记录"""
    metric = models.ForeignKey(Metrics, verbose_name='指标名', on_delete=models.CASCADE)
    execution_time = models.DateTimeField(auto_now_add=True, verbose_name='实际执行时间')
    execution_period = models.CharField(verbose_name='执行周期', max_length=20)
    value = models.IntegerField(verbose_name='统计结果')

    class Meta:
        verbose_name = '指标统计结果'
        verbose_name_plural = verbose_name
        unique_together = ['metric', 'execution_period']

    def __str__(self):
        return self.metric.metric


class MetricMethod(models.Model):
    """指标统计方法定义"""
    metric = models.OneToOneField(Metrics, verbose_name='指标名', on_delete=models.CASCADE)
    data_source = models.CharField(verbose_name='数据源名称', max_length=20)
    address = models.GenericIPAddressField(verbose_name='数据源IP')
    user = models.CharField(verbose_name='用户', max_length=10)
    password = models.CharField(verbose_name='密码', max_length=20)
    db_type = models.CharField(verbose_name='数据库类型', choices=DatabaseTypes.choices,
                               default=DatabaseTypes.DB2, max_length=20)
    db_name = models.CharField(verbose_name='数据库名', max_length=10)
    port = models.IntegerField(verbose_name='数据库端口')
    stmt = models.TextField(verbose_name='统计SQL语句')
    date_parm_flag = models.BooleanField(verbose_name='日期参数标识', default=True)
    # extra_detail_table_flag = models.BooleanField(verbose_name='额外明细存储标识', default=False)

    class Meta:
        verbose_name = '指标统计方法'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.metric.metric


class IdaStatistics(models.Model):
    """自助取数平台各行按月统计结果"""
    period = models.CharField(verbose_name='统计周期', max_length=20)
    org_no = models.CharField(verbose_name='机构号', max_length=12)
    org_name = models.CharField(verbose_name='机构名称', max_length=50)
    query_count = models.IntegerField(verbose_name='查询次数')
    download_count = models.IntegerField(verbose_name='下载次数')

    class Meta:
        verbose_name = '自助取数明细统计'
        verbose_name_plural = verbose_name
        ordering = ['period', 'org_no']

    def __str__(self):
        return self.org_no + self.period

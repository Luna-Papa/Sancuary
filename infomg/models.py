from django.db import models


# Create your models here.


class ProductDefect(models.Model):
    """基础软件缺陷总表"""
    periods = models.CharField(max_length=7, verbose_name='期数')
    # number = models.IntegerField(verbose_name='序号')
    category = models.CharField(verbose_name='产品类型', max_length=50)
    model = models.CharField(verbose_name='设备型号/软件版本', max_length=200)
    manufacturer = models.CharField(max_length=100, verbose_name='生产厂商')
    reason = models.TextField(verbose_name='缺陷原因')
    defect = models.CharField(max_length=20, verbose_name='缺陷影响')
    solution = models.TextField(verbose_name='解决方案')
    fix_pack = models.CharField(max_length=200, verbose_name='补丁版本')
    status = models.CharField(max_length=10, verbose_name='解决状态')
    find_date = models.DateField(verbose_name='发现时间')
    v_solution = models.CharField(max_length=200, verbose_name='行内解决方案', null=True)
    # v_flag = models.BooleanField(verbose_name='行内解决状态', default=False)
    v_flag = models.CharField(verbose_name='行内解决状态',
                              choices=((0, '待解决'), (1, '已解决'), (2, '无需处理')), max_length=1)

    def __str__(self):
        return self.model

    class Meta:
        verbose_name = '基础软硬件产品缺陷信息表'
        verbose_name_plural = verbose_name
        unique_together = (
            'periods', 'category', 'model', 'manufacturer', 'defect',
            'fix_pack', 'status', 'find_date',
        )


class DefectDetail(models.Model):
    """缺陷明细记录表"""
    periods = models.CharField(max_length=7, verbose_name='期数')
    model = models.ForeignKey(ProductDefect, on_delete=models.CASCADE, verbose_name='设备型号/软件版本')
    system = models.CharField(verbose_name='涉及系统', max_length=10)
    solution = models.TextField(verbose_name='解决方案', null=True)
    status = models.BooleanField(verbose_name='解决状态', default=False)
    solve_date = models.DateField(verbose_name='拟解决日期', null=True)
    solved_date = models.DateField(verbose_name='解决日期', null=True)

    def __str__(self):
        return self.system

    class Meta:
        verbose_name = '缺陷明细记录表'
        verbose_name_plural = verbose_name
        unique_together = (
            'periods', 'model', 'system',
        )

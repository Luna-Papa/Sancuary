from django.db import models
from django.contrib.auth.models import AbstractUser
from rbac.models import Role


# Create your models here.


class UserInfo(AbstractUser):
    org_id = models.CharField(max_length=20, verbose_name='所属机构编号', null=True)
    real_name = models.CharField(max_length=50, verbose_name='真实姓名', null=True)
    department = models.CharField(max_length=100, verbose_name='部门', null=True)
    position = models.CharField(max_length=50, verbose_name='职位', null=True)
    phone = models.CharField(max_length=20, verbose_name='联系方式', null=True)
    email = models.EmailField(max_length=100, verbose_name='邮箱', blank=True)
    roles = models.ManyToManyField(verbose_name='拥有角色', to=Role, blank=True)

    class Meta:
        verbose_name = '用户管理'
        verbose_name_plural = verbose_name
        ordering = ['username']

    def __str__(self):
        return self.username


class Slogan(models.Model):
    text = models.CharField(verbose_name='标语', max_length=200, unique=True)
    v_flag = models.BooleanField(verbose_name='有效标识')
    created_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_time = models.DateTimeField(auto_now=True, verbose_name='上次修改时间')

    class Meta:
        verbose_name = '标语管理'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.text

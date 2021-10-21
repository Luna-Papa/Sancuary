from django.db import models

# Create your models here.


class Permission(models.Model):
    """权限表"""
    # seq = models.SmallIntegerField(verbose_name='菜单顺序', null=True, blank=True)
    title = models.CharField(max_length=32, unique=True, verbose_name='权限名称')
    url = models.CharField(max_length=128, unique=True, verbose_name='URL')
    perm_code = models.CharField(max_length=32, unique=True, verbose_name='URL别名')
    is_menu = models.BooleanField(verbose_name="是否是菜单", default=True)
    perm_group = models.ForeignKey(to='PermGroup', blank=True, on_delete=models.CASCADE, verbose_name='所属权限组')
    pid = models.ForeignKey(to='Permission', blank=True, on_delete=models.CASCADE,
                            verbose_name='所属二级菜单', null=True)  # pid为空，则该条记录为二级菜单

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = '权限表'
        verbose_name_plural = verbose_name


class Role(models.Model):
    """角色表"""
    title = models.CharField(max_length=32, unique=True, verbose_name='角色名')
    permissions = models.ManyToManyField(verbose_name='角色拥有权限', to='Permission', blank=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "角色表"
        verbose_name_plural = verbose_name


class PermGroup(models.Model):
    """权限组表"""
    title = models.CharField(max_length=32, verbose_name='组名称')
    menu = models.ForeignKey(to='Menu', verbose_name='组所属菜单', blank=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = '权限组'
        verbose_name_plural = verbose_name


class Menu(models.Model):
    """一级菜单名称"""
    title = models.CharField(max_length=32, unique=True, verbose_name='一级菜单')
    icon = models.CharField(max_length=32, verbose_name='图标', blank=True)

    class Meta:
        verbose_name = '一级菜单'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.title

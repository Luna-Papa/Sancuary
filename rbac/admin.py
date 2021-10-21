from django.contrib import admin
from rbac.models import Permission, PermGroup, Role, Menu
# Register your models here.


@admin.register(Permission)
class PermissionAdmin(admin.ModelAdmin):
    list_display = ['title', 'url', 'perm_code', 'perm_group', 'pid', 'is_menu']
    fields = ['title', 'url', 'perm_code', 'perm_group', 'pid', 'is_menu']


@admin.register(PermGroup)
class PermGroupAdmin(admin.ModelAdmin):
    list_display = ['title', 'menu']
    fields = ['title', 'menu']


admin.site.register(Role)


@admin.register(Menu)
class MenuAdmin(admin.ModelAdmin):
    list_display = ['title', 'icon']
    fields = ['title', 'icon']

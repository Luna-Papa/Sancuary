from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from dataexp.models import SystemInfo
# Register your models here.


@admin.register(SystemInfo)
class SystemInfoAdmin(admin.ModelAdmin):
    list_display = ('sys_name', 'chn_name', 'db_type', 'db_name', 'address', 'port', 'codepage', 'val_flag')
    fields = ('sys_name', 'chn_name', 'db_type', 'db_name', 'address', 'port', 'codepage',
              'username', 'password', 'val_flag')
    search_fields = ['sys_name', 'chn_name', 'db_name']
    list_filter = ('sys_name', 'chn_name', 'db_name')



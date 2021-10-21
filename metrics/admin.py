from django.contrib import admin
from .models import Metrics, MetricMethod, MetricsDetail
# Register your models here.


@admin.register(Metrics)
class MetricsAdmin(admin.ModelAdmin):
    list_display = ('metric', 'chn_name', 'period', 'v_flag', 'created_time', 'updated_time')


@admin.register(MetricMethod)
class MetricMethodAdmin(admin.ModelAdmin):
    list_display = ('metric', 'data_source', 'address', 'user', 'password',
                    'db_type', 'db_name', 'port', 'stmt')

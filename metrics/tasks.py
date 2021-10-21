import datetime
from celery import shared_task
#####################################################################
import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Sanctuary.settings")
from django.core.wsgi import get_wsgi_application

application = get_wsgi_application()
#####################################################################
from metrics.models import Metrics, MetricsDetail, MetricMethod, IdaStatistics
from utils.db_conn import execute_sql
from utils.date import get_metric_date


@shared_task(name='metric.metric_execute', queue='metric')
def metric_execute(period):
    current_period, begin_date, end_date = get_metric_date(period)
    # 根据指标周期和有效标识取出要处理的指标
    metrics = Metrics.objects.filter(period=period, v_flag=True, special_flag=False)
    if metrics.exists():
        for metric in metrics:
            metric_method_obj = MetricMethod.objects.filter(pk=metric.id)
            address, user, password, db_type, db_name, port, stmt = \
                list(metric_method_obj.values_list('address', 'user',
                                                   'password', 'db_type', 'db_name', 'port', 'stmt'))[0]
            results = execute_sql(db_type, user, password, db_name, stmt, address, port, begin_date, end_date)
            if results:
                metric_result = results[0]
                MetricsDetail.objects.update_or_create(
                    metric=metric, execution_period=current_period, value=metric_result)


@shared_task(name='metric.ida_statistics', queue='metric')
def ida_statistics():
    """定时取自助取数平台各农商行和村镇银行使用数据"""
    period, begin_date, end_date = get_metric_date('month')
    try:
        method_obj = MetricMethod.objects.filter(metric__metric='ida_statistics')
        address, user, password, db_type, db_name, port, stmt = \
            list(method_obj.values_list('address', 'user',
                                        'password', 'db_type', 'db_name', 'port', 'stmt'))[0]
        results = execute_sql(db_type, user, password, db_name, stmt, address, port, begin_date, end_date)
        for line in results:
            org_no, org_name,  query_count, download_count = line
            IdaStatistics.objects.update_or_create(period=period, org_no=org_no, org_name=org_name,
                                                   query_count=query_count, download_count=download_count)
    except Exception as e:
        print(e)

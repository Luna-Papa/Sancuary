from django.shortcuts import render, HttpResponse
from .models import Metrics, MetricsDetail, IdaStatistics
from django.db.models import Q
import datetime
import json


# Create your views here.


def data_service(request):
    today = datetime.datetime.today()
    if request.method == 'GET':
        current_period = (today.replace(day=1) - datetime.timedelta(days=1)).strftime('%Y-%m')
        last_period = (today.replace(day=1) - datetime.timedelta(days=31)).strftime('%Y-%m')
        zzqs_login_count_last_month = \
            MetricsDetail.objects.get(execution_period=last_period,
                                      metric__metric='zzqs_login_count').value
        zzqs_query_count_last_month = \
            MetricsDetail.objects.get(execution_period=last_period,
                                      metric__metric='zzqs_query_count').value
        zzqs_download_count_last_month = \
            MetricsDetail.objects.get(execution_period=last_period,
                                      metric__metric='zzqs_download_count').value
        zzqs_login_count_current_month = \
            MetricsDetail.objects.get(execution_period=current_period,
                                      metric__metric='zzqs_login_count').value
        zzqs_query_count_current_month = \
            MetricsDetail.objects.get(execution_period=current_period,
                                      metric__metric='zzqs_query_count').value
        zzqs_download_count_current_month = \
            MetricsDetail.objects.get(execution_period=current_period,
                                      metric__metric='zzqs_download_count').value
        context = {
            'nsyh_sjxf_user_count':
                MetricsDetail.objects.get(execution_period=current_period,
                                          metric__metric='nsyh_sjxf_user_count').value,
            'czyh_sjxf_user_count':
                MetricsDetail.objects.get(execution_period=current_period,
                                          metric__metric='czyh_sjxf_user_count').value,
            'sjxf_app_count':
                MetricsDetail.objects.get(execution_period=current_period,
                                          metric__metric='sjxf_app_count').value,
            'sjxf_table_count':
                MetricsDetail.objects.get(execution_period=current_period,
                                          metric__metric='sjxf_table_count').value,
            'zzqs_login_count': zzqs_login_count_current_month,
            'zzqs_query_count': zzqs_query_count_current_month,
            'zzqs_download_count': zzqs_download_count_current_month,
            'zzqs_login_count_increase':
                (zzqs_login_count_current_month - zzqs_login_count_last_month) /
                zzqs_login_count_last_month,
            'zzqs_query_count_increase':
                (zzqs_query_count_current_month - zzqs_query_count_last_month) /
                zzqs_query_count_last_month,
            'zzqs_download_increase':
                (zzqs_download_count_current_month - zzqs_download_count_last_month) /
                zzqs_download_count_last_month,
            'ida_statics': IdaStatistics.objects.filter(period=current_period)
        }
        return render(request, 'dashboard/data_service.html', context=context)
    elif request.method == 'POST':
        year = request.POST.get('year')
        if year == 'this_year':
            period = today.strftime('%Y')
        elif year == 'last_year':
            period = \
                (today.replace(month=1).replace(day=1) - datetime.timedelta(days=1)).strftime('%Y')  # 获取去年年份
        else:
            period = year
        zzqs_data = []
        zzqs_objects = MetricsDetail.objects.filter(execution_period__startswith=period).filter(
            Q(metric__metric='zzqs_login_count') |
            Q(metric__metric='zzqs_query_count') |
            Q(metric__metric='zzqs_download_count')
        )
        periods = zzqs_objects.values('execution_period').distinct()
        period_list = []
        for period in periods:
            period_list.append(period['execution_period'])
        for period in period_list:
            zzqs_data.append({
                'period': period,
                'zzqs_login_count': MetricsDetail.objects.get(execution_period=period,
                                                              metric__metric='zzqs_login_count').value,
                'zzqs_query_count': MetricsDetail.objects.get(execution_period=period,
                                                              metric__metric='zzqs_query_count').value,
                'zzqs_download_count': MetricsDetail.objects.get(execution_period=period,
                                                                 metric__metric='zzqs_download_count').value
            })
        return HttpResponse(json.dumps(zzqs_data), content_type="application/json")


def get_ida_statics(request):
    if request.method == 'POST':
        ida_statics_list = []
        period = request.POST.get('period')
        if period:
            ida_statics = IdaStatistics.objects.filter(period=period)
            for ida in ida_statics:
                ida_statics_list.append({
                    'org_no': ida.org_no,
                    'org_name': ida.org_name,
                    'query_count': ida.query_count,
                    'download_count': ida.download_count,
                })
            return HttpResponse(json.dumps(ida_statics_list), content_type="application/json")

from django.urls import path
from dataquery.views import sfcx, pos, account


app_name = 'DataQuery'
urlpatterns = [
    path('sfcx/', sfcx, name='sfcx'),  # 对手信息查询
    path('pos/', pos, name='pos'),  # POS商户信息查询
    path('account/', account, name='account'),  # 开户信息查询
]

from django.urls import path
from .views import data_service, get_ida_statics
app_name = 'dashboard'

urlpatterns = [
    path('data_service/', data_service, name='data_service'),  # 展示数据下发和自助取数服务统计数据
    path('ida_statics/', get_ida_statics, name='get_ida_statics'),
]


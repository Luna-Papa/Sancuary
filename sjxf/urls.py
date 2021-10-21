from django.urls import path
from .views import BaseTablesView, ManualSjxf, ajax_data_relations, TaskListView, \
    DataRelationView, DataUsersView


app_name = 'sjxf'
urlpatterns = [
    path('basetables/', BaseTablesView.as_view(), name='base_table'),  # 展示已下发基础表
    path('datarelations/', DataRelationView.as_view(), name='data_relation'),  # 展示下发关系 - 农商银行与数据表 【网页初始化】
    path('manual-sjxf/', ManualSjxf.as_view(), name='manual_sjxf'),  # 手工全量数据下发
    path('get_data_relations/', ajax_data_relations, name='filter_data_relation'),  # 展示下发关系 - 农商银行与数据表 【实际数据请求-ajax】
    path('task_list/', TaskListView.as_view(), name='task_list'),  # 展示用户已创建的数据下发任务
    path('user_list/', DataUsersView.as_view(), name='user_list'),  # 展示数据下发接入用户
]

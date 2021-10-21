from django.urls import path
from infomg.views import *


app_name = 'InfoMG'
urlpatterns = [
    path('defect_import/', defect_import, name='defect_imp'),  # 基础软硬件缺陷导入
    path('defect_list/', defect_list, name='defect_list'),  # 基础软硬件缺陷查看
    path('defect_detail/', defect_detail, name='defect_detail'),  # 缺陷明细查看
    path('add_defect_detail/', add_defect_detail, name='default_add_defect_detail'),  # 增加产品/软件待处理记录
    path('add_defect_detail/<int:defect_id>/', add_defect_detail, name='add_defect_detail'),  # 增加产品/软件待处理记录 - 页面跳转
    path('ajax_get_defect/', ajax_get_defect, name='ajax_get_defect'),  # 根据缺陷期数筛选具体缺陷列表
    path('save_defect_detail/', save_defect_detail, name='save_defect_detail'),  # 保存待处理缺陷记录
    path('delete_defect_detail/', ajax_dlt_defect_detail, name='dlt_defect_detail'),  # 删除待处理缺陷记录
    path('add_detail_solved_date/', ajax_update_solved_date, name='add_solved_date'),  # 修改待处理缺陷记录的实际解决日期
    path('update_defect_v_solution/', ajax_update_v_solution, name='add_v_solution'),  # 添加产品缺陷记录的行内解决方案
    path('update_defect_v_flag/', ajax_update_defect_v_flag, name='update_defect_v_flag'),  # 更新产品缺陷记录的行内解决状态
]

from django.shortcuts import render, HttpResponse
from django.http import JsonResponse
from django.views.generic import View
from .models import DataSub, DataUsers, BaseTables, DataRelation, TaskList, StatusTypes
from users.models import UserInfo
from sjxf.tasks import data_push
import json
import uuid
# Create your views here.


class BaseTablesView(View):
    """下发表列表"""

    def get(self, request):
        all_tables = BaseTables.objects.filter(flag=0)
        return render(request, 'sjxf/basetables.html', {'all_tables': all_tables})


class DataUsersView(View):
    """数据下发接入"""

    def get(self, request):
        all_users = DataUsers.objects.all()
        return render(request, 'sjxf/datausers.html', {'all_users': all_users})


class ManualSjxf(View):
    def get(self, request):
        users = list(DataUsers.objects.all().values('user_id', 'org_name'))
        tables = list(BaseTables.objects.filter(flag=0).values('id', 'ds_id', 'table_name'))
        context = {
            'data_users': users,
            'tables': tables,
            # 'sjxf_nav_active': True,
        }
        return render(request, 'sjxf/manualSJXF.html', context=context)

    def post(self, request):
        all_tasks = []
        username = request.user.username if request.user.username else 'admin'
        userinfo = UserInfo.objects.filter(username=username)
        if userinfo.exists():
            real_name = UserInfo.objects.get(username=username).real_name
        else:
            real_name = '手工下发'
        for organ in request.POST.getlist('org_no'):
            for table in request.POST.getlist('table_id'):
                # task_id = uuid.uuid4()
                # 取出后台全量数据下发任务所需参数值
                #     1 渠道名称：  DS_ID
                #     2 机构  号：  DUSER_ID
                #     3 数据表名：  TBNAME
                #     4 数据表ID:   T_ID
                queryset = BaseTables.objects.get(id=table)
                ds_id = queryset.ds_id
                tb_name = queryset.table_name
                # t_id = queryset.id
                # 检验数据表与下发机构是否匹配
                result = DataSub.objects.filter(user_id=organ, t_id=table)
                remarks = ''
                task_id = uuid.uuid4()
                if not result.exists():
                    remarks = f'该行未配置下发表{tb_name}'
                    status = StatusTypes.status_cancel
                    celery_task_id = ''
                else:
                    # 调用celery异步任务
                    push = data_push.delay(ds_id, organ, tb_name, table, task_id)
                    status = StatusTypes.status_submit
                    celery_task_id = push.task_id
                task = TaskList(task_id=task_id, user_id=username, user_name=real_name,
                                org_no=organ, table_name=tb_name, status=status,
                                remarks=remarks, celery_task_id=celery_task_id)
                task.save()
                all_tasks.append(TaskList.objects.get(task_id=task_id))
        return render(request, 'sjxf/tasklist.html', {'all_tasks': all_tasks})


class DataRelationView(View):
    def get(self, request):
        return render(request, 'sjxf/datarelations.html')


def ajax_data_relations(request):
    relation_list = []
    if request.method == 'POST':
        org_no = request.POST.get('org_no')
        table_name = request.POST.get('table_name')
        if org_no:
            relations = DataRelation.objects.filter(user_id=org_no)  # 按机构号精准匹配
        elif table_name:
            if len(table_name.strip()) >= 4:
                relations = DataRelation.objects.filter(table_name__icontains=table_name)  # 按表名模糊匹配
            else:
                relations = []
        else:
            relations = DataRelation.objects.all()[:200]  # 默认返回数据表前200条记录进行展示
        for relation_info in relations:
            relation_list.append({
                'user_id': relation_info.user_id,
                'org_name': relation_info.org_name,
                'ds_id': relation_info.ds_id,
                'table_name': relation_info.table_name,
                # 'c_user_id': relation_info.c_user_id,
                # 前端ajax请求datetime格式数据需要转换
                'create_date':
                    relation_info.create_date.strftime('%Y-%m-%d %H:%M:%S')
                    if relation_info.create_date
                    else '',
            })
        return HttpResponse(json.dumps(relation_list), content_type="application/json")


class TaskListView(View):
    def get(self, request):
        username = request.user.username
        all_tasks = TaskList.objects.filter(user_id=username)
        return render(request, 'sjxf/tasklist.html', {'all_tasks': all_tasks})

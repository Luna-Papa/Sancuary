from django.shortcuts import render
from django.http import HttpResponse, FileResponse
from django.views.generic import View
from django.db import transaction
from dataexp.models import SystemInfo, ExpTaskList
from users.models import UserInfo
from django.utils.http import urlquote
import xlrd
import uuid


# Create your views here.


def exp_register(request):
    if request.method == "GET":
        systems = SystemInfo.objects.filter(val_flag=True)
        context = {
            'systems': systems,
            'data_exp_nav_active': True,
        }
        return render(request, 'dataexp/registration.html', context=context)
    elif request.method == "POST":
        register_type = request.POST.get("register_type")
        if register_type == 'manual':
            task_no = uuid.uuid4()
            sys_name = SystemInfo.objects.get(sys_name=request.POST.get("sys_name"))
            user_name = request.user.username if request.user.username else 'admin'
            real_name = UserInfo.objects.get(username=user_name)
            file_type = request.POST.get("file_type") if request.POST.get("file_type") else 'ixf'
            exp_method = request.POST.get("exp_method") if request.POST.get("exp_method") else 'hpu'
            code_page = request.POST.get("codepage") if request.POST.get("codepage") else '1386'
            delimiter = request.POST.get("delimiter")
            separator = request.POST.get("separator")
            work_date = request.POST.get("work_date")
            table_counts = int(request.POST.get("table_counts"))
            for i in range(1, table_counts + 1):
                table_name = request.POST.get(f"table_{i}")
                task = ExpTaskList(task_no=task_no, user_id=user_name, username=real_name,
                                   sys_name=sys_name, table_name=table_name, file_type=file_type,
                                   exp_method=exp_method, code_page=code_page, delimiter=delimiter,
                                   separator=separator, work_date=work_date)
                task.save()
            all_tasks = ExpTaskList.objects.filter(task_no=task_no).values()
            return render(request, "dataexp/tasklist.html", {'all_tasks': all_tasks, 'data_exp_nav_active': True})
        elif register_type == 'upload':
            f = request.FILES.get('file')
            excel_type = f.name.split('.')[1]
            if excel_type in ['xls', 'xlsx']:
                wb = xlrd.open_workbook(filename=None, file_contents=f.read())
                table = wb.sheets()[0]
                rows = table.nrows
                try:
                    task_no = uuid.uuid4()
                    with transaction.atomic():
                        user_name = request.user.username if request.user.username else 'admin'
                        real_name = UserInfo.objects.get(username=user_name).real_name \
                            if UserInfo.objects.get(username=user_name).real_name else 'admin'
                        for i in range(1, rows):
                            i_row = table.row_values(i)
                            # 处理入表ExpTaskList所需字段
                            sys_name = i_row[0]
                            table_name = i_row[1]
                            file_type = i_row[2] if i_row[2] else 'ixf'
                            exp_method = i_row[3] if i_row[3] else 'hpu'
                            code_page = i_row[4] if i_row[4] else '1208'
                            delimiter = i_row[5]
                            separator = i_row[6]
                            work_date = i_row[7]
                            task = ExpTaskList(task_no=task_no, user_id=user_name, username=real_name,
                                               sys_name=sys_name, table_name=table_name, file_type=file_type,
                                               exp_method=exp_method, code_page=code_page, delimiter=delimiter,
                                               separator=separator, work_date=work_date)
                            task.save()
                    all_tasks = ExpTaskList.objects.filter(task_no=task_no).values()
                    return render(request, "dataexp/tasklist.html",
                                  {'all_tasks': all_tasks, 'data_exp_nav_active': True})
                except Exception as e:
                    print(e)


def download_template(request):
    """下载文件上传模板"""
    file = open('static/files/template_dataexp.xlsx', 'rb')
    response = FileResponse(file)
    response['Content-Type'] = 'application/octet-stream'
    filename_chinese = "填写模板"
    response['Content-Disposition'] = 'attachment;filename="%s.xlsx"' % (urlquote(filename_chinese))
    return response


class TaskListView(View):
    def get(self, request):
        username = request.user.username
        all_tasks = ExpTaskList.objects.filter(user_id=username)
        return render(request, 'dataexp/tasklist.html', {'all_tasks': all_tasks, 'data_exp_nav_active': True})

from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from infomg.models import ProductDefect, DefectDetail
from django.db import transaction
import xlrd
from xlrd import xldate_as_tuple
from datetime import datetime
import json
from django.http import JsonResponse
from django.urls import reverse


# Create your views here.


def defect_import(request):
    """导入软硬件缺陷列表"""
    if request.method == 'GET':
        return render(request, 'infomg/defect_imp.html')
    elif request.method == 'POST':
        f = request.FILES.get('file')
        periods = request.POST.get('periods')
        excel_type = f.name.split('.')[-1]
        if excel_type in ['xls', 'xlsx']:
            wb = xlrd.open_workbook(filename=None, file_contents=f.read())
            table = wb.sheets()[0]
            rows = table.nrows
            try:
                with transaction.atomic():
                    for i in range(3, rows):
                        i_row = table.row_values(i)
                        try:
                            number = int(i_row[0])
                        except Exception as e:
                            break
                        category = i_row[1]
                        if category not in ['数据库', '中间件', '其它']:  # 只关注数据库、中间件和其它这三个产品类型
                            continue
                        try:
                            model = i_row[2].replace('\n', ' ')
                        except Exception as e:
                            model = i_row[2]
                        manufacturer = i_row[3]
                        reason = i_row[4].replace('\n', ' ')
                        defect = i_row[5]
                        solution = i_row[6].replace('\n', ' ')
                        try:
                            fix_pack = i_row[7].replace('\n', ' ')
                        except Exception as e:
                            fix_pack = i_row[7]
                        status = i_row[8]
                        find_date = datetime(*xldate_as_tuple(i_row[9], 0))
                        task = ProductDefect(periods=periods, category=category, model=model,
                                             manufacturer=manufacturer, reason=reason,
                                             defect=defect, solution=solution, fix_pack=fix_pack,
                                             status=status, find_date=find_date)
                        task.save()
                all_defects = ProductDefect.objects.filter(periods=periods).values()
                return HttpResponseRedirect(reverse('InfoMG:defect_list'),
                                            {'all_defects': all_defects, 'periods': periods})
            except Exception as e:
                print(e)


def defect_list(request):
    """展示软硬件缺陷列表"""
    if request.method == 'GET':
        all_defects = ProductDefect.objects.all().values()
        all_details_count = 0  # 计算一条缺陷下创建待处理明细条数
        solved_details_count = 0  # 待处理明细已处理数量
        for defect in all_defects:
            try:
                details = DefectDetail.objects.filter(model=defect['id'])
                all_details_count = details.count()  # 计算一条缺陷下创建待处理明细条数
                for detail in details:
                    if detail.status:
                        solved_details_count += 1
            except Exception as e:
                pass
            defect['all_details_count'] = all_details_count
            defect['solved_details_count'] = solved_details_count
        return render(request, 'infomg/defect_list.html', {'all_defects': all_defects})


def defect_detail(request):
    details = DefectDetail.objects.all()
    return render(request, 'infomg/defect_detail.html', {'details': details})


def add_defect_detail(request, defect_id=None):
    if request.method == 'GET':
        if defect_id:
            defects = ProductDefect.objects.get(pk=defect_id)
            return render(request, 'infomg/add_defect_detail.html', {'defects': defects})
        else:
            defects = ProductDefect.objects.all()
            periods = ProductDefect.objects.all().values('periods').distinct()
            return render(request, 'infomg/add_defect_detail.html', {'defects': defects, 'periods': periods})


def ajax_get_defect(request):
    periods = request.POST.get('periods')
    defect_models = list(ProductDefect.objects.filter(periods=periods).values('model'))
    return HttpResponse(json.dumps(defect_models), content_type="application/json")


def save_defect_detail(request):
    if request.method == 'POST':
        systems = request.POST.getlist('system')
        solutions = request.POST.getlist('solution')
        solve_dates = request.POST.getlist('solve_date')
        periods = request.POST.get('periods')
        defect_model = request.POST.get('defect_model')
        defect_model_id = ProductDefect.objects.get(model=defect_model, periods=periods)
        counts = len(systems)
        for i in range(0, counts):
            DefectDetail.objects.create(periods=periods, model=defect_model_id, system=systems[i],
                                        solution=solutions[i], solve_date=solve_dates[i])
        details = DefectDetail.objects.filter(periods=periods)
        # return render(request, 'infomg/defect_detail.html', {'details': details})
        return HttpResponseRedirect(reverse('InfoMG:defect_detail'), {'details': details})


def ajax_dlt_defect_detail(request):
    if request.method == 'POST':
        defect_id = request.POST.get('defect_id')
        try:
            # periods = DefectDetail.objects.get(pk=defect_id).periods
            DefectDetail.objects.get(pk=defect_id).delete()
            # detail_obj = DefectDetail.objects.filter(periods=periods)
            return HttpResponse('success')
        except Exception as e:
            return HttpResponse('failed')


def ajax_update_solved_date(request):
    if request.method == 'POST':
        detail_id = request.POST.get('detail_id')
        solved_date = request.POST.get('solved_date')
        DefectDetail.objects.filter(pk=detail_id).update(solved_date=solved_date, status=True)
        # 如果一条缺陷对应的待处理明细都已经解决，则该缺陷应被修改为已完成。
        defect_id = DefectDetail.objects.get(pk=detail_id).model_id
        periods = DefectDetail.objects.get(pk=detail_id).periods
        if not DefectDetail.objects.filter(model=defect_id, periods=periods, status=False):
            ProductDefect.objects.filter(pk=defect_id).update(v_flag=True)
        return HttpResponse('success')


def ajax_update_v_solution(request):
    """更新产品缺陷的整体解决方案"""
    if request.method == 'POST':
        defect_id = request.POST.get('defect_id')
        v_solution = request.POST.get('v_solution')
        try:
            ProductDefect.objects.filter(pk=defect_id).update(v_solution=v_solution, v_flag=0)
            return HttpResponse('success')
        except Exception as e:
            return HttpResponse('failed')


def ajax_update_defect_v_flag(request):
    """更新产品缺陷的行内处理状态"""
    if request.method == 'POST':
        defect_id = request.POST.get('defect_id')
        v_solution = request.POST.get('v_solution')
        try:
            ProductDefect.objects.filter(pk=defect_id).update(v_flag=2, v_solution=v_solution)
            return HttpResponse('success')
        except Exception as e:
            return HttpResponse('failed')

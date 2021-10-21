from django.shortcuts import render
from django.views.generic.base import View
from django.views.generic import ListView
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from users.models import UserInfo
from rbac.server.init_permission import init_permission
# Create your views here.


def index(request):
    return render(request, 'sjxf/basetables.html')


def user_login(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                # 登录
                login(request, user)
                init_permission(request, user)
                return HttpResponseRedirect(reverse('sjxf:base_table'))
            else:
                return render(request, 'users/login.html', {'msg': '密码输入错误'})
        else:
            return render(request, 'users/login.html', {'msg': '用户不存在'})

    elif request.method == 'GET':
        return render(request, 'users/login.html')


def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('users:login'))


class ModifyPwdView(View):
    """修改用户密码"""
    def post(self, request):
        pwd2 = request.POST.get("password2", "")
        user_id = request.user.username
        user = UserInfo.objects.get(username=user_id)
        user.password = make_password(pwd2)
        user.save()
        return HttpResponseRedirect(reverse('users:login'))


def check_passwd(request):
    if request.method == 'POST':
        user_name = request.user.username
        old_pwd = request.POST.get("password", "")
        user = authenticate(username=user_name, password=old_pwd)
        if not user:
            msg = '原密码输入有误'
            return HttpResponse(msg)
        else:
            return HttpResponse('ok')

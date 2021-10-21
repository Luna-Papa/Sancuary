from django.urls import path
from users.views import user_login, user_logout, ModifyPwdView, check_passwd


app_name = 'users'
urlpatterns = [
    path('login/', user_login, name='login'),  # 用户登录
    path('logout/', user_logout, name='logout'),  # 用户退出登录
    path('chg_pwd/', ModifyPwdView.as_view(), name='chg_pwd'),  # 用户修改密码
    path('check_pwd/', check_passwd, name='chk_pwd'),  # ajax校验密码
]

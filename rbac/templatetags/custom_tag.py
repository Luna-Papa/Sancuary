from django import template
from django.conf import settings
import re
import os
from django.utils.safestring import mark_safe

register = template.Library()  # 生成模板类库


def get_structure_data(request):
    current_url = request.path_info  # 取出当前请求的URL
    perm_menu = request.session[settings.PERMISSION_MENU_KEY]  # 取出init_permission生成的数据，列表类型，每项均为字典类型
    menu_dict = {}

    for item in perm_menu:
        if not item['pid_id']:
            menu_dict[item['id']] = item.copy()

    for item in perm_menu:
        regex = "^{0}$".format(item["url"])
        if re.match(regex, current_url):
            if not item["pid_id"]:
                menu_dict[item["id"]]["active"] = True
            else:
                menu_dict[item["pid_id"]]["active"] = True

    menu_result = {}
    for item in menu_dict.values():
        active = item.get("active")
        menu_id = item.get("menu_id")
        if menu_id in menu_result:
            menu_result[menu_id]["children"].append({'title': item["title"],
                                                     'url': item["url"], 'active': active})
            if active:
                menu_result[menu_id]["active"] = True
        else:
            menu_result[menu_id] = {
                'menu_id': menu_id,
                'menu_title': item["menu_title"],
                'active': active,
                'icon': item['menu_icon'],
                'children': [
                    {'title': item["title"], 'url': item["url"], 'active': active}
                ]
            }
    return menu_result


@register.inclusion_tag('users/rbac_menu.html')
def rbac_menu(request):
    menu_data = get_structure_data(request)
    return {'menu_result': menu_data}

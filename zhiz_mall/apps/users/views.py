from django.shortcuts import render
from django.views import View
from apps.users.models import User
from django.http import JsonResponse
from django.contrib.auth import login, logout, authenticate

import json
import re


# Create your views here.
class UserCountView(View):
    '''用户是否重复'''
    def get(self, request, username):
        # 查询数据库
        count = User.objects.filter(username=username).count()
        # 返回结果
        if count > 0:
            return JsonResponse({'count':count, 'code': 400, 'errmsg': '用户名已存在'})
        else:
            return JsonResponse({'count':count, 'code': 0, 'errmsg': 'ok'})


class RegisterView(View):
    '''用户注册'''
    def post(self, request):
        data = json.loads(request.body.decode())
        # 获取参数
        username = data.get('username')
        password = data.get('password')
        password2 = data.get('password2')
        mobile = data.get('mobile')
        allow = data.get('allow')
        # 校验参数
        if not all([username, password, password2, mobile, allow]):
            return JsonResponse({'code': 400, 'errmsg': '缺少必传参数'})
        # 校验用户名是否满足规则
        if not re.match(r'^[a-zA-Z0-9_-]{5,20}$', username):
            return JsonResponse({'code': 400, 'errmsg': '用户名不满足规则'})
        
        # # 校验密码是否满足规则
        # if not re.match(r'^[0-9A-Za-z]{8,20}$', password):
        #     return JsonResponse({'code': 400, 'errmsg': '密码不满足规则'})
        # # 校验两次密码是否一致
        # if password != password2:
        #     return JsonResponse({'code': 400, 'errmsg': '两次密码不一致'})
        # # 校验手机号是否满足规则
        # if not re.match(r'^1[3-9]\d{9}$', mobile):
        #     return JsonResponse({'code': 400, 'errmsg': '手机号不满足规则'})
        # # 校验是否同意协议
        # if allow != 'true':
        #     return JsonResponse({'code': 400, 'errmsg': '必须同意协议'})
        # 保存用户数据
        user = User.objects.create_user(username=username, password=password, mobile=mobile)
        login(request, user)
        

        # 返回结果
        return JsonResponse({'code': 0, 'errmsg': 'ok'})

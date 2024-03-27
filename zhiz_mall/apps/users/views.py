from django.shortcuts import render
from django.views import View
from apps.users.models import User
from django.http import JsonResponse
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


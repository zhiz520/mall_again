from django.http import JsonResponse
from django.shortcuts import render
from django.views import View

from apps.areas.models import Area

# Create your views here.
class AreaView(View):
    '''省级'''
    def get(self, request):
        pass


class SubAreaView(View):
    '''市级'''
    def get(self, request):
        # 获取数据
        provinces = Area.objects.filter(parent=None)
        province_list = []
        for province in provinces:
            province_list.append({
                'id': province.id,
                'name': province.name,
            })
        

        # 响应
        return JsonResponse({'code': 0, 'errmsg': 'ok', 'province_list': province_list})
    

class SubAreaView(View):
    '''市级'''
    def get(self, request, province_id):
        # 获取数据
        up_level = Area.objects.get(id=province_id)
        down_level = up_level.subs.all()
        down_list = []
        for down in down_level:
            down_list.append({
                'id': down.id,
                'name': down.name,
            })

        # 响应
        return JsonResponse({'code': 0, 'errmsg': 'ok', 'sub_data': {'subs': down_list}})
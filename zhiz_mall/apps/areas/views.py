from django.http import JsonResponse
from django.shortcuts import render
from django.views import View
from django.core.cache import cache

from apps.areas.models import Area

# Create your views here.

class AreaView(View):
    '''市级'''
    def get(self, request):
        # 获取缓存
        data = cache.get('province_list')
        print(type(data))
        if data is not None:
            return JsonResponse({'code': 0, 'errmsg': 'ok', 'province_list': data})
        # 获取数据
        provinces = Area.objects.filter(parent=None)
        province_list = []
        for province in provinces:
            province_list.append({
                'id': province.id,
                'name': province.name,
            })
        # 设置缓存
        cache.set('province_list', province_list, 3600 * 24)

        # 响应
        return JsonResponse({'code': 0, 'errmsg': 'ok', 'province_list': province_list})
    

class SubAreaView(View):
    '''市级'''
    def get(self, request, id):
        # 获取缓存
        data = cache.get('sub_data_{}'.format(id))
        if data:
            return JsonResponse({'code': 0, 'errmsg': 'ok', 'sub_data': data})
        # 获取数据
        up_level = Area.objects.get(id=id)
        down_level = up_level.subs.all()
        down_list = []
        for down in down_level:
            down_list.append({
                'id': down.id,
                'name': down.name,
            })
        # 设置缓存
        cache.set('sub_data_{}'.format(id), down_list, 3600 * 24)
        # 响应
        return JsonResponse({'code': 0, 'errmsg': 'ok', 'sub_data': {'subs': down_list}})
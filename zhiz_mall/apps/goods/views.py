from django.shortcuts import render
from django.views import View
from utils.goods import get_categories
from apps.contents.models import ContentCategory


# Create your views here.
class IndexView(View):
    def get(self, request):
        '''
        首页数据分2部分
        1， 广告
        2， 商品分类
        '''
        # 1， 广告数据
        contents = {}

        categories = get_categories()
        for cat in categories:
            contents[cat.key] = cat.content_set.filter(status=True).order_by('sequence')

        # 数据传给模板
        context = {
            'categories': categories,
            'contents': contents
        }

        return render(request, 'index.html', context)
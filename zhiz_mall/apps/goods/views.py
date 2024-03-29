from django.http import JsonResponse
from django.shortcuts import render
from django.views import View
from utils.goods import get_breadcrumb, get_categories
from apps.contents.models import ContentCategory
from apps.goods.models import SKU

from django.core.paginator import Paginator

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
    

class ListView(View):
    '''
    商品列表页
    '''
    def get(self, request, category_id):

        # 查询字段
        ordering = request.GET.get('ordering')
        # 每页数据数量
        page_size = request.GET.get('page_size') 
        # 要第几页数据
        page = request.GET.get('page')
        # 根据就id获取category对象
        try:
            category = ContentCategory.objects.get(id=category_id)
        except ContentCategory.DoesNotExist:
            return JsonResponse({'code': 400, 'errmsg': '参数缺失'})
        
        # 获取面包屑数据
        breadcrumb = get_breadcrumb(category)

        # 查询对应的sku数据， 然后排序， 分页
        
        skus = SKU.objects.filter(category=category, is_launched=True).order_by(ordering)
        # 分页
        paginator = Paginator(sku, per_page=page_size)
        
        # 获取第page页的数据
        page_sku = paginator.page(page)
        
        # 将对象转换字典数据
        sku_list = []
        for sku in skus:
            sku_list.append({
                'id': sku.id,
                'name': sku.name,
                'price': sku.price,
                'default_image_url': sku.default_image.url
            })

        # 获取总页数
        total_num = paginator.num_pages
        return JsonResponse({
            'code': 0, 'errmsg': 'ok', 'list': sku_list, 'count': total_num, 'breadcrumb': breadcrumb
        })

        
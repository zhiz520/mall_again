from django.http import JsonResponse
from django.shortcuts import render
from django.views import View
from utils.goods import get_breadcrumb, get_categories
from apps.contents.models import ContentCategory
from apps.goods.models import SKU

from django.core.paginator import Paginator
from django.template import loader
from haystack.views import SearchView

from zhiz_mall import settings
import os

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
        for sku in page_sku.object_list:
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

        
class HotView(View):
    '''
    热销排行
    '''
    def get(self, request, category_id):

        # 获取category对象
        try:
            category = ContentCategory.objects.get(id=category_id)
        except ContentCategory.DoesNotExist:
            return JsonResponse({'code': 400, 'errmsg': '参数缺失'})
        
        # 查询对应的sku数据， 然后排序
        skus = SKU.objects.filter(category=category, is_launched=True).order_by('-sales')[:3] # 根据sales字段的值排序
        
        # 将对象转换字典数据
        sku_list = []
        for sku in skus:
            sku_list.append({
                'id': sku.id,
                'name': sku.name,
                'price': sku.price,
                'default_image_url': sku.default_image.url
            })
        
        return JsonResponse({'code': 0, 'errmsg': 'ok', 'hot_skus': sku_list})

# 配合搜索引擎实现全文检索, 原理， 设置关键字和搜索词条的对应关系，并记录位置， 类似清华字典 elsaticsearch
# 数据和搜索引擎的中间桥梁： Haystack

class SKUSearchView(SearchView):

    def create_response(self):
        """
        Generates the actual HttpResponse to send back to the user.
        """

        context = self.get_context()
        # 转化json数据
        context_list = []
        for sku in context['page'].object_list:
            context_list.append({

                # 'id': sku.id,
                # 'name': sku.object.name,
                # 'price': sku.object.price,
                # 'default_image_url': sku.object.default_image.url,
                # 'searchkey': sku.object.get('query'),
                # 'page_size': context['page'].paginator.num_pages,
                # 'count': context['page'].paginator.count;
                'id': sku.object.id,
                'name': sku.object.name,
                'price': sku.object.price,
                'default_image_url': sku.object.default_image.url,
                'searchkey': sku.context.get('query'),
                'page_size': context['page'].paginator.num_pages,
                'count': context['page'].paginator.count

            })

        return JsonResponse(context_list, safe=False)
    

# 静态化渲染
def generic_zhiz_index():
    # 1， 广告数据
    contents = {}

    categories = get_categories()
    for cat in categories:
        contents[cat.key] = cat.content_set.filter(status=True).order_by('sequence')


    context = {
        'categories': categories,
        'contents': contents
    }
    # 1.加载渲染的模板
    index_tamplate = loader.get_template('index.html')

    # 2.把数据给模板
    index_html_data = index_tamplate.render(context)

    # 3.把渲染好的html， 写入指定文件
    file_path = os.path.join(os.path.dirname(settings.BASE_DIR), 'front_end_pc/index.html')

    with open(file_path, 'w') as f:
        f.write(index_html_data)



    
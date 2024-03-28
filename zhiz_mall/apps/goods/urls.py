from django.urls import path

from mall_again.zhiz_mall.apps.goods.views import IndexView


urlpatterns = [
    path('index/', IndexView.as_view()),
    
]
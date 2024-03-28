from django.urls import path
from apps.areas.views import AreaView, SubAreaView 

urlpatterns = [
    path('areas/', AreaView.as_view()),  # 省市区三级联动
    path('areas/<id>/', SubAreaView.as_view()),  # 省市区三级联动
]
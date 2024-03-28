from django.shortcuts import render
from django.views import View
from apps.users.models import User, Address
from django.http import JsonResponse
from django.contrib.auth import login, logout, authenticate
from django.core.mail import send_mail
from django.core.serializers import serialize

from utils.crypts1 import crypt_encode, crypt_decode
from utils.views1 import LoginJsonMixin
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
    

class LoginView(View):
    '''用户登录'''
    def post(self, request):
        # 获取数据
        data = json.loads(request.body.decode())
        username = data.get('username')
        password = data.get('password')
        remembered = data.get('remembered')

        # 检验数据
        if not all([username, password]):
            return JsonResponse({'code': 400, 'errmsg': '缺少必传参数'})
        # 检查是用户名是否手机号
        if re.match(r'^1[3-9]\d{9}$', username):
            User.USERNAME_FIELD = 'mobile'
        else:
            User.USERNAME_FIELD = 'username'

        user = authenticate(username=username, password=password)
        if user is None:
            return JsonResponse({'code': 400, 'errmsg': '用户名或密码错误'})
        # login
        login(request, user)

        # 判断是否记住用户登录
        if remembered is None:
            request.session.set_expiry(0)
        else:
            request.session.set_expiry(None)

        # 返回相应
        response = JsonResponse({'code': 0, 'errmsg': 'ok'})
        response.set_cookie('username', user.username, max_age=7*24*3600)
        return response
    

class LogoutView(View):
    '''用户退出'''
    def delete(self, request):
        logout(request)
        # 删除cookie
        response = JsonResponse({'code': 0, 'errmsg': 'ok'})
        response.delete_cookie('username')
        return response
        
    
class CenterView(LoginJsonMixin, View):
    '''用户中心'''
    def get(self, request):
        
        info_data = {
            'username': request.user.username,
            'mobile': request.user.mobile,
            'email': request.user.email,
            'email_active': request.user.email_active
        }

        return JsonResponse({'code': 0, 'errmsg': 'ok', 'info_data': info_data})
    

class EmailView(LoginJsonMixin, View):
    '''邮箱'''
    def put(self, request):
        # 获取参数
        data = json.loads(request.body.decode())
        email = data.get('email')
        # 校验参数
        if not email:
            return JsonResponse({'code': 400, 'errmsg': '缺少email参数'})
        # 校验邮箱是否满足规则
        if not re.match(r'^[a-z0-9][\w\.\-]*@[a-z0-9\-]+(\.[a-z]{2,5}){1,2}$', email):
            return JsonResponse({'code': 400, 'errmsg': '邮箱不满足规则'})
        # 保存邮箱
        user = request.user
        user.email = email
        user.save()
        # 发送激活邮件
        # 加密email
        token = crypt_encode(user.id)
        # 激活链接
        html_message = '点击激活 <a href=http://www.zhiz.com/?token={}> 激活</a>'.format(token)
        send_mail('枝枝邮箱验证', '', 'qi_rui_hua@163.com', [email], html_message='')

        # 返回结果
        return JsonResponse({'code': 0, 'errmsg': 'ok'})


class EmailVerifyView(View):
    '''邮箱验证'''
    def put(self, request):
        # 获取参数
        data = json.loads(request.body.decode())
        token = data.get('token')
        # 校验参数
        if not token:
            return JsonResponse({'code': 400, 'errmsg': '缺少token参数'})
        
        # 解密token
        user_id = crypt_encode(token)
        # 查询数据库
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return JsonResponse({'code': 400, 'errmsg': '无效的token'})
        # 修改邮箱激活状态
        user.email_active = True
        user.save()
        # 返回结果
        return JsonResponse({'code': 0, 'errmsg': 'ok'})


class AddressCreateView(View):
    '''新增地址'''
    def post(self, request):
        # 获取参数
        data = json.loads(request.body.decode())
        receiver = data.get('receiver')
        province_id = data.get('province_id')
        city_id = data.get('city_id')
        district_id = data.get('district_id')
        place = data.get('place')
        mobile = data.get('mobile')
        tel = data.get('tel')
        email = data.get('email')

        # 校验参数
        if not all([receiver, province_id, city_id, district_id, place, mobile]):
            return JsonResponse({'code': 400, 'errmsg': '缺少必传参数'})
        
        if not re.match(r'^1[3-9]\d{9}$', mobile):
            return JsonResponse({'code': 400, 'errmsg': '手机号不满足规则'})
        
        # 数据入库
        user = request.user
        addresses = Address.objects.create(
            user=user,
            title=receiver,
            receiver=receiver,
            province_id=province_id,
            city_id=city_id,
            district_id=district_id,
            place=place,
            mobile=mobile,
            tel=tel,
            email=email
        )
        # 设置返回Json数据
        address_dict = {
            "id": addresses.id,
            "title": addresses.title,
            "receiver": addresses.receiver,
            "province": addresses.province.name,
            "city": addresses.city.name,
            "district": addresses.district.name,
            "place": addresses.place,
            "mobile": addresses.mobile,
            "tel": addresses.tel,
            "email": addresses.email
        }

        # 返回结果
        return JsonResponse({'code': 0, 'errmsg': 'ok', 'addresses': address_dict})


class AddressView(View):
    '''查询视图'''
    def get(self, request):
        # 获取参数
        user = request.user
        # 查询地址
        addresses = Address.objects.filter(user=user, is_deleted=False)
        # 构造返回数据
        address_list = []
        for address in addresses:
            address_list.append({
                "id": address.id,
                "title": address.title,
                "receiver": address.receiver,
                "province": address.province.name,
                "city": address.city.name,
                "district": address.district.name,
                "place": address.place,
                "mobile": address.mobile,
                "tel": address.tel,
                "email": address.email
            })
            
        # 返回结果
        return JsonResponse({'code': 0, 'errmsg': 'ok', 'addresses': address_list})
    

class AddressUpdateView(View):
    '''修改地址'''
    def put(self, request, address_id):
        # 获取参数
        data = json.loads(request.body.decode())
        try:
            address = Address.objects.get(id=address_id)
        except Address.DoesNotExist:
            return JsonResponse({'code': 400, 'errmsg': '地址不存在'})
        
        # 修改地址
        for key, value in data.items():
            if hasattr(address, key):
                setattr(address, key, value)
        address.save()
        # 返回结果
        return JsonResponse({'code': 0, 'errmsg': 'ok'})


class AddressDeleteView(View):
    '''删除地址'''
    def delete(self, request, address_id):
        # 获取参数
        try:
            address = Address.objects.get(id=address_id)
            # 修改地址
            address.is_deleted = True
            address.save()
            
        except Address.DoesNotExist:
            return JsonResponse({'code': 400, 'errmsg': '地址不存在'})
        # 返回结果
        return JsonResponse({'code': 0, 'errmsg': 'ok'})
    

class AddressDefaultView(View):
    '''设置默认地址'''
    def put(self, request, address_id):
        # 获取参数
        try:
            address = Address.objects.get(id=address_id)
            # 修改地址
            user = request.user
            user.default_address = address
            user.save()
            
        except Address.DoesNotExist:
            return JsonResponse({'code': 400, 'errmsg': '地址不存在'})
        # 返回结果
        return JsonResponse({'code': 0, 'errmsg': 'ok'})
    



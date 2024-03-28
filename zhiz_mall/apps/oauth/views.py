import json
from django.http import JsonResponse
from django.shortcuts import render
from apps.oauth.models import QQUser
from django.views import View
from QQLoginTool.QQtool import OAuthQQ
from django.contrib.auth import login
from zhiz_mall import settings
from apps.users.models import User

from utils.crypts1 import crypt_decode, crypt_encode

# Create your views here.
class QQLoginUrlView(View):
    '''QQ登录'''
    def get(self, request):
        # 实例化qq对象
        qq = OAuthQQ(
            client_id=settings.QQ_CLIENT_ID,
            client_secret=settings.QQ_CLIENT_SECRET,
            redirect_uri=settings.QQ_REDIRECT_URI,
            # state=settings.QQ_STATE
        )
        # 生成链接
        qq_login_url = qq.get_qq_url()
        # 响应
        return JsonResponse({'code': 0, 'errmsg': 'OK', 'login_url': qq_login_url})


class OauthQQView(View):
    '''QQ登录回调'''
    def get(self, request):
        # 接收参数
        code = request.GET.get('code')
        if code is None:
            return JsonResponse({'code': 400, 'errmsg': '缺少参数'})
        # 实例化qq对象
        qq = OAuthQQ(
            client_id=settings.QQ_CLIENT_ID,
            client_secret=settings.QQ_CLIENT_SECRET,
            redirect_uri=settings.QQ_REDIRECT_URI,
            # state=settings.QQ_STATE
        )
        
        # 获取token
        token = qq.get_access_token(code)
        # get open id
        openid = qq.get_open_id(token)
        # 根据openid判断是否绑定用户
        crypt_openid = crypt_encode(openid)
        try:
            qquser = QQUser.objects.get(openid=openid)
        except QQUser.DoesNotExist:
            return JsonResponse({'code': 400, 'errmsg': '用户不存在'})
        else:
            login(request, qquser)
            response = JsonResponse({'code': 0, 'errmsg': 'OK', 'access_token': crypt_openid})
            response.set_cookie('username', qquser.username, max_age=3600 * 24)
            
            return response
        
    def post(self, request):
        data = json.loads(request.body.decode())
        mobile = data.get('mobile')
        password = data.get('password')
        openid = crypt_decode(data.get('access_token'))

        # 检验是否绑定
        try:
            user = User.objects.get(mobile=mobile)
        except User.DoesNotExist:
            user = User.objects.create_user(username=mobile, password=password, mobile=mobile)
        else:
            if not user.check_password(password):
                return JsonResponse({'code': 400, 'errmsg': '用户名或密码错误'})
        
        QQUser.objects.create(user=user, openid=openid)

        login(request, user)

        response = JsonResponse({'code': 0, 'errmsg': 'OK'})
        response.set_cookie('username', user.username, max_age=3600 * 24)
        return response

import random
from django.shortcuts import render
from django.views import View
from libs.captcha.captcha import captcha
from libs.yuntongxun.sms import CCP

from django.http import HttpResponse, JsonResponse
from django_redis import get_redis_connection
from celerys_task.sms.tasks import celery_sms_code

# Create your views here.
class ImageCodeView(View):
    '''图片验证码'''
    def get(self, request, uuid):
        # 生成图片验证码
        # 调用captcha生成图片验证码
        # 生成图片验证码
        text, image = captcha.generate_captcha()
        # 保存图片验证码
        redis_cli = get_redis_connection('code')
        redis_cli.setex(uuid, 3000, text)
        # 返回图片二进制文件, 响应体类型,content_type
        return HttpResponse(image, content_type='image/jpeg')


class SmsCodeView(View):
    '''短信验证码'''
    def get(self, request, mobile):
    # 获取图片验证码
        img_code = request.GET.get('image_code')
        uuid = request.GET.get('image_code_id')
        # 获取redis中的图片验证码
        redis_cli = get_redis_connection('code')
        code = redis_cli.get(uuid)
        if code is None:
            return JsonResponse({'code': 400, 'errmsg': '图片验证码过期'})
        print('\n', type(code), '\n')
        if code.decode().lower() != img_code.lower():
            return JsonResponse({'code': 400, 'errmsg': '图片验证码错误'})
        # 提取标记检查是否短时间内再次注册
        send_flag = redis_cli.get('send_flag_{}'.format(mobile))
        if send_flag is not None:
            return JsonResponse({'code': 400, 'errmsg': '请求过于频繁'})
        
        # 生成短信验证码
        sms_code = '%06d' % random.randint(0, 999999)
        # 保存短信验证码
        # redis_cli.setex('sms_{}'.format(mobile), 3000, sms_code)
        # # 设置标记防止频繁注册
        # redis_cli.setex('send_flag_{}'.format(mobile), 60, 1)
        # 使用pipelin管道技术
        pipeline = redis_cli.pipeline()
        pipeline.setex('sms_{}'.format(mobile), 3000, sms_code)
        pipeline.setex('send_flag_{}'.format(mobile), 60, 1)
        pipeline.execute()
        # 发送短信验证码
        # CCP().send_template_sms(mobile, [sms_code, 5], 1)
        celery_sms_code.delay(mobile, sms_code)
        
        # 返回响应
        return JsonResponse({'code': 0, 'errmsg': 'ok'})


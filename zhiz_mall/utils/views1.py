from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse


class LoginJsonMixin(LoginRequiredMixin):

    def handle_no_permission(self):
        return JsonResponse({'code': 400, 'errmsg': '没登录'})
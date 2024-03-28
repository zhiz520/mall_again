from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
# class User(models.Model):
#     '''用户模型类'''
#     username = models.CharField(max_length=20, unqiue=True, verbose_name='用户名')
#     password = models.CharField(max_length=40, verbose_name='密码')
#     mobile = models.CharField(max_length=11, unique=True, verbose_name='手机号')

#     class Meta:
#         db_table = 'tb_users'
#         verbose_name = '用户'
#         verbose_name_plural = verbose_name

#     def __str__(self):
#         return self.username
    
class User(AbstractUser):
    mobile = models.CharField(max_length=11, unique=True, verbose_name='手机号')
    email_active = models.BooleanField(default=False, verbose_name='邮箱验证状态')

    class Meta:
        db_table = 'tb_users'
        verbose_name = '用户'
        verbose_name_plural = verbose_name


from celery import Celery
import os


# 设置路径
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'zhiz_mall.settings')


# 创建实例
app = Celery('celerys_task')

# 设置broker
app.config_from_object('celerys_task.configs')

# 让celery检测包
app.autodiscover_tasks(['celerys_task.sms', 'celerys_task.emailss'])
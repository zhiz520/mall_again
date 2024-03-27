from libs.yuntongxun.sms import CCP
from celerys_task.main import app


@app.task
def celery_sms_code(mobile, sms):
    '''短信异步'''
    CCP().send_template_sms(mobile, [sms, 5], 1)
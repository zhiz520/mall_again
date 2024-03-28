from celerys_task.main import app
from django.core.mail import send_mail


@app.task
def send_email_async(recipient_list, subject='枝枝大宝贝', message='枝枝今天也很棒！', from_email='qi_rui_hua@163.com', html_message=None):
    send_mail(subject, message, from_email, recipient_list, html_message=html_message)
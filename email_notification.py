import smtplib
from email.message import EmailMessage
from datetime import datetime

def generate_test_email(to_addr):
    date_str = datetime.now().strftime('%Y.%m.%d')
    time_str = datetime.now().strftime('%Y.%m.%d-%H:%M:%S')

    msg = EmailMessage()
    msg['Subject'] = '您已启用出入校自动填报邮件通知功能'
    msg['From'] = 'noreply@pku.epidemic.everyday'
    msg['To'] = to_addr
    
    msg.set_content('''您好！

    如果您收到这封邮件，说明您可以正常使用填报失败时的邮件通知功能。请尽情享受程序自动化带来的便利。

    如果您不知道这是什么，请忽略这封邮件，非常抱歉。

    非常感谢，祝您愉快。
    {0}
    '''.format(time_str))
    return msg

def generate_error_email(err_backtrace, to_addr):
    date_str = datetime.now().strftime('%Y.%m.%d')
    time_str = datetime.now().strftime('%Y.%m.%d-%H:%M:%S')

    msg = EmailMessage()
    msg['Subject'] = '{0}出入校自动填报失败通知'.format(date_str)
    msg['From'] = 'noreply@pku.epidemic.everyday'
    msg['To'] = to_addr
    
    msg.set_content('''您好！

    如果您收到这封邮件，说明您今天（{0}）的出入校填报程序执行失败了。您可以：
    - 检查网络后重新执行程序 / 手动填报园区往返
    - 在我的github上获取最新版的程序
    - 把这封邮件转给我 / 发github issue通知我。

    如果您不知道这是什么，请忽略这封邮件，非常抱歉。

    非常感谢，祝您愉快。

    错误日志：
    {1}
    '''.format(time_str, err_backtrace))
    return msg

def send_email(msg, smtp_server, smtp_login):
    '''
    '''
    s = smtplib.SMTP(smtp_server)
    s.login(*smtp_login)
    s.send_message(msg)
    s.quit()


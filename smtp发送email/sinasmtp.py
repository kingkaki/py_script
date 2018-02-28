#encoding=utf8
import smtplib
from email.mime.text import MIMEText

msg_from ='15xxxxx@sina.cn' #发送方邮箱
passwd ='xxxxxxxx' #填入发送方邮箱的授权码
msg_to = 'xxxxxx@qq.com'  #收件人邮箱
                            
subject = "xxxxxxxxx" #主题     
content = 'xxxxxxxxxxxx' #正文

msg = MIMEText(content)
msg['Subject'] = subject
msg['From'] = msg_from
msg['To'] = msg_to

s = smtplib.SMTP("smtp.sina.cn", 25)           #邮件服务器及端口号
s.login(msg_from, passwd)                      
for i in range(100):
	s.sendmail(msg_from, [msg_to], msg.as_string())
	print("%d email has been sended "% i)


s.quit()

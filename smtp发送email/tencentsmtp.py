#encoding=utf8
import smtplib, requests
from email.mime.text import MIMEText

msg_from ='hxxxxxxxxxx@qq.com' #发送方邮箱
passwd ='axxxxxxxx' #填入发送方邮箱的授权码
msg_to ='8xxxxxxx@qq.com'  #收件人邮箱
                            
subject = "xxxx" #主题     
content = 'xxxxxxxxx' #正文
msg = MIMEText(content, 'plain', 'utf-8')
msg['Subject'] = subject
msg['From'] = msg_from
msg['To'] = msg_to

s = smtplib.SMTP_SSL("smtp.qq.com", 465)           #邮件服务器及端口号
s.login(msg_from, passwd)
for i in range(100):
	s.sendmail(msg_from, [msg_to], msg.as_string())
	print("%d email has been sended "% i)

s.quit()


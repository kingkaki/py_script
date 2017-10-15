#-*-coding:utf-8-*- 
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import requests,re

domain = "https://www.194ff.com"
url = "https://www.194ff.com/htm/piclist9"

p = requests.get(url)
# print p.text
r=re.compile('<a href="(/htm.pic9.*?)" target="_blank">')
items = re.findall(r,p.text)
picitems =[] #存放子链接的urls
for item in items:
	picitems.append(domain + item)

for item in picitems:#子链接中遍历图片并下载	
	p2 = requests.get(item)
	#print p2.text
	r2 =re.compile('src="(https://pic.bb164.com/d6/3386/.*?)"')
	picurls =  re.findall(r2,p2.text)
	from  contextlib import closing
	x=1
	for pic in picurls:
		with closing(requests.get(pic,stream=True))  as response:#下载图片
			with open("D:\\pic\\"+str(x)+".jpg","wb") as fd:
				for chunk in response.iter_content(128):
					fd.write(chunk)
				print pic+"is ok"
				x+=1	

	

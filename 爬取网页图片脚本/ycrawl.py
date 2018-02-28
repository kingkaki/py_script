#encoding=utf

import re, threading, time

import requests

thread_num =20
base_dir = ''

lock = threading.Lock()
domain = "https://www.586aa.com"
root_urls = []
headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:56.0) Gecko/20100101 Firefox/56.0"}
page_urls = set()
pic_urls = set()
succeed_key = 0
faild_key = 0
len_pics = 0

def collect_rooturl():
	global root_urls, base_dir
	base_dir = input("请先输入存放路径,格式 D:/image/:")+"/"
	sort = input('''1：亚洲图片
2：欧美图片
3：卡通动漫
4：性爱乱伦
7：美腿丝袜
8：清纯唯美
9：偷拍自拍
请输入需要的种类代号（1-9）:''')
	start_page = input("请输入起始页码")
	end_page = input("请输入末尾页码")
	for i in range(int(start_page), int(end_page)+1):
		url = "%s/htm/piclist%s/%d.htm" % (domain,sort,i)
		root_urls.append(url)

def mkdir(path):
    """
    创建目录
    """
    import os
    isExists=os.path.exists(path)
    if not isExists:
        os.makedirs(path) 
        return True
    else:
        return False

def create_filename(url):
    """
    通过url转换成完整的文件地址
    """
    path = url.replace("https://pic.bb164.com/", "")
    path = path.replace('/', '_',2)
    filename = base_dir+path
    mkdir(re.sub(r'(-\d+\.jpg)',"",filename))
    filename = filename.replace('-','/')
    return filename

def collect_pageurls():
	global page_urls
	for root_url in root_urls:
		r = requests.get(root_url, headers=headers)
		urls = re.findall(r'<a href="(/htm/pic\d/\d+.htm)" target="_blank">', r.text)
		for url in urls:
			page_urls.add(domain+url)

def collect_picurls(url):
	global pic_urls
	r = requests.get(url, headers=headers)
	urls = re.findall(r'src="(https://pic\.bb164\.com/.*?\.jpg)">',r.text)
	for url in urls:
		pic_urls.add(url)

def down_thread():
	global succeed_key, faild_key
	for url in pic_urls:
		try:
			r = requests.get(url, stream=True, timeout=1)
			if r.status_code == 404:
				with lock:
					faild_key+=1
				continue
			filename = create_filename(url)
			with open(filename, 'wb') as f:
				for chunk in r.iter_content(1024):
					f.write(chunk)
			with lock:
				succeed_key += 1
				print("%d/%d is downed(faild %d)" % (succeed_key,len_pics,faild_key),end="\r")
		except:
			with lock:
				faild_key += 1

def thread_start():
	thread_list = []
	for i in range(thread_num):
		t = threading.Thread(target=down_thread)
		thread_list.append(t)
	for t in thread_list:
		t.start()
	for t in thread_list:
		t.join()

def main():
	start_time = time.time()
	global page_urls, pic_urls,len_pics	
	collect_rooturl()
	print("preparing……it'll just take a moment")
	collect_pageurls()
	for url in page_urls:
		collect_picurls(url)
	len_pics = len(pic_urls)
	pic_urls = (url for url in pic_urls)
	print("\r")
	thread_start()
	end_time = time.time()
	consume_time = end_time - start_time 
	print("all done,%d is succeed,%d is faild,consume %.2fseconds" % (succeed_key,faild_key,consume_time))

if __name__ == '__main__':
	main()
#encoding=utf8
import requests, re, threading

root_url = "http://www.xicidaili.com/wn/"
headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:56.0) Gecko/20100101 Firefox/56.0"}
lock = threading.Lock()

def find_proxies(page_num=3):
	'''
	返回包含ip：port的字典生成器
	'''
	proxy_pool = set()
	for i in range(1,page_num+1):
		r = requests.get(root_url, headers=headers)
		proxies = re.findall(r'<td>(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})</td>\s+<td>(\d+)</td>', r.text)	
		for proxy in proxies:
			ip, port = proxy #tuple拆包
			proxy_pool.add(proxy)
	iter_pool = (proxy for proxy in proxy_pool)
	return iter_pool

def checkout_thread(iter_pool,timeout=1):
	'''
	检查代理是否有用
	'''
	for proxy in iter_pool:
		ip, port = proxy
		proxies = {"http":"{ip}:{port}".format(ip=ip,port=port),
					"https":"{ip}:{port}".format(ip=ip,port=port)}
		try:
			r = requests.get("http://www.baidu.com",headers=headers,proxies=proxies,timeout=timeout)
			print(proxy)
		except:
			pass

def deal_thread(iter_pool,thread_num=100,timeout=1):
	'''
	开启、等待线程，默认线程数100
	'''
	thread_list = []
	for i in range(thread_num):
		t = threading.Thread(target=checkout_thread,args=(iter_pool,timeout))
		thread_list.append(t)
	for t in thread_list:
		t.start()
	for t in thread_list:
		t.join()

def main():
	iter_pool = find_proxies()
	deal_thread(iter_pool,timeout=0.5)
	
if __name__ == '__main__':
	main()
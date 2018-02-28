#encoding=utf8
import os ,time,requests ,re,threading

url = 'http://localhost/wooyun/bugs.php'
header = {'User-Agent':'Mozilla/5.0(compatible;MSIE9.0;WindowsNT6.1;Trident/5.0'}
thread_list = []
thread_num = 4
all_page = 295

def search_wybug(start ,end):
	start_time = time.time()
	print('task thread (%s)...' % (threading.current_thread()))
	for i in range(start, end):
		with open('d:/bugs.txt','a+') as f:
			r = requests.get(url, params = {'page':i},headers=header)
			r.encoding = 'utf8'
			bugs = re.findall(r'<a href="bug_detail.*?">(.*?)</a>',r.text)
			for bug in bugs:
				f.write(bug.rstrip()+'\n')
		print('done %d page' % i)
	end_time = time.time()
	print('Task %s runs %0.2f seconds.' % (threading.current_thread(), (end_time - start_time)))

def main():
	start_time = time.time()
	for i in range(thread_num):
		start = i*(all_page//thread_num)
		end = (i+1)*((all_page//thread_num)-1)
		t = threading.Thread(target=search_wybug, args=(start,end))
		thread_list.append(t)
	for t in thread_list:
		t.start()
	for t in thread_list:
		t.join()
	end_time = time.time()
	print("all consume %0.2f seconds" % (end_time - start_time))

if __name__ == '__main__':
	main()
#encoding=utf8
from  multiprocessing import Pool
import os ,time,requests ,re,threading

url = 'http://localhost/wooyun/bugs.php'
header = {'User-Agent':'Mozilla/5.0(compatible;MSIE9.0;WindowsNT6.1;Trident/5.0'}
thread_list = []
core_num = 4
thread_num = 5
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

def sw_thread(start ,end):
	print('task pid (%s)...' % (os.getpid()))
	for i in range(thread_num):
		thread_start = start+i*((end-start)//thread_num)
		thread_end = start+(i+1)*((end-start)//thread_num)
		t = threading.Thread(target=search_wybug, args=(thread_start,thread_end))
		thread_list.append(t)
	for t in thread_list:
		t.start()
	for t in thread_list:
		t.join()

def main():
	print('parent process %s' % os.getpid())
	start_time = time.time()
	p = Pool()
	for i in range(core_num):
		start = i*(all_page//core_num)
		end = (i+1)*((all_page//core_num)-1)
		p.apply_async(sw_thread,args=(start,end))
	print('waiting for all subprocesses done……')
	p.close()
	p.join()
	end_time = time.time()
	print('All consume %0.2f second' % (end_time - start_time))


if __name__ == '__main__':
	main()
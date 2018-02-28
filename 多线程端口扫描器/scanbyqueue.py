#encoding=utf8
import socket, threading, time
from queue import Queue

thread_num = 800
port_num = 65535
ipORdomain = '127.0.0.1'
timeout = 0.5

alive_port = set()
close_port = set()
lock = threading.Lock()
key = 0

q = Queue()

def create_ipqueue():
	global q
	for i in range(1,port_num+1):
		q.put(i)

def scan_thread():
	global q
	global key
	while not q.empty():
		i = q.get()
		try:
			sk = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			sk.settimeout(timeout)
			sk.connect((ipORdomain,i))
			alive_port.add(i)
		except Exception:
			close_port.add(i)
		sk.close()		
		with lock:
			key+=1
			print("%d/%d ports has been scaned……" % (key, port_num) ,end="\r");

	print("100%!finish!", end="\r");
						

def main():
	start_time = time.time()
	create_ipqueue()
	thread_list = []
	for i in range(thread_num):
		t = threading.Thread(target=scan_thread)
		thread_list.append(t)
	for t in thread_list:
		t.start()
	for t in thread_list:
		t.join()
	print('alive ports are {}'.format(sorted(alive_port)))
	print('close ports nums {}'.format(len(close_port)))
	end_time = time.time()
	print('all consumne %.2f seconds' % (end_time - start_time))
	
if __name__ == '__main__':
	main()

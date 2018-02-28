#encoding=utf8
import socket, threading ,time

thread_num = 800
port_num = 2535
ipORdomain = '106.14.162.156'
timeout = 0.5

alive_port = set()
close_port = set()
lock = threading.Lock()
key = 0

def scan_thread(start, end ):
	for i in range(start, end):
		try:
			sk = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			sk.settimeout(timeout)
			sk.connect((ipORdomain,i))
			alive_port.add(i)
		except Exception:

			close_port.add(i)
		sk.close()
		
		global key
		with lock:
			key+=1
			print("%d/%d ports has been scaned……" % (key, port_num) ,end="\r");

	print("100%!finish!", end="\r");
						

def main():
	start_time = time.time()
	thread_list = []
	for i in range(thread_num):
		start = i*round(port_num/thread_num)
		end = (i+1)*(round(port_num/thread_num))
		t = threading.Thread(target=scan_thread, args=(start, end))
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

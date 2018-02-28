#encoding=utf8
__author__ = 'kingkk'

import requests, re, threading, time

#可修改配置
root_url = 'http://www.mmjpg.com/home/5'
thread_num = 10
base_dir = 'd:/'



#默认参数设置（请勿修改）
headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:56.0) Gecko/20100101 Firefox/56.0"}
succeed_key = 0
faild_key = 0
broken_key = 0
len_pics = 0
pics_url_pool = set()
pages_url_set = set()
lock = threading.Lock()



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


def get_pics_url(url):
    """
    通过子页面生成图片url
    """
    global pics_url_pool
    try:
        r = requests.get(url, headers=headers, timeout=1)
        r.encoding = 'utf8'
        max_num = re.findall(r'>(\d+)</a>',r.text)[-1]
        base_url = re.search(r'src="(http://img\.mmjpg.com/\d+/\d+/)\d+\.jpg"',r.text)
        if base_url is not None:
            base_url = base_url.group(1)
        else:
            print("%s can be analyzed…"%url)
            return
        i=1
        while i<=int(max_num):
            pics_url_pool.add("%s%d.jpg"%(base_url,i))
            i+=1
    except:
        print("%s is useless…"%url)


def get_pages_url():
    """
    通过主页面生成子页面url
    """
    global pages_url_set
    r = requests.get(root_url, headers=headers)
    pages_url = re.findall(r'<a href="(http://www.mmjpg.com/mm/\d+)" target="_blank">',r.text)
    for page_url in pages_url:
        pages_url_set.add(page_url)


def create_filename(url):
    """
    通过url转换成完整的文件地址
    """
    path = url.replace("http://img.mmjpg.com/", "")
    path = path.replace('/', '_',1)
    filename = base_dir+path
    mkdir(re.sub(r'(/\d+\.jpg)',"",filename))
    return filename


def down_thread():
    """
    通过图片的url下载图片
    """
    global succeed_key, len_pics, faild_key, broken_key
    for pic_url in pics_url_pool:
        try:
            r = requests.get(pic_url, stream=True, timeout = 1)
            if r.headers['content-length'] == '63675':
                with lock:
                    broken_key+=1
                continue
            filename = create_filename(pic_url)
            with open(filename, 'wb') as f:
                for chunk in r.iter_content(1024):   
                     f.write(chunk)
            with lock:
                succeed_key +=1
                print("%d/%d is downed(faild %d broken %d)" % (succeed_key, len_pics, faild_key, broken_key), end='\r')
        except:
            faild_key+=1


def thread_start():
    """
    添加、开启、等待线程
    """
    thread_list = []
    for i in range(thread_num):
        t = threading.Thread(target=down_thread)
        thread_list.append(t)
    for t in thread_list:
        t.start()
    for t in thread_list:
        t.join()


def main():
    global pages_url_set, pics_url_pool, len_pics
    print("preparing……it'll just take a moment")
    get_pages_url()  #获取子页面url

    for i in pages_url_set:   #获取每个图片url
        get_pics_url(i) 

    print("\r")
    len_pics = len(pics_url_pool)
    pics_url_pool = (i for i in pics_url_pool)

    thread_start()

    print("all done,%d is succeed,%d is failed,%d pics are broken" % (succeed_key, faild_key, broken_key), end=",")


if __name__ == '__main__':
    start_time = time.time()
    main()
    end_time = time.time()
    print("totally consume %0.2f second" % (end_time - start_time))

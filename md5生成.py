#encoding=utf8
import string
import re
from hashlib import md5
import random

def foo():
    t=0
    m=0
    cset = string.letters+string.digits
    s='XIPU'
    while True:
        m+=1
        for i in cset:
            tmp=s+i
            x = md5(tmp).hexdigest()[8:24]
            if re.match(r'0e\d{14}',x):
                print tmp
                t=1
                break
        s+=random.choice(cset)
        #print m
        if t==1:
            break
foo()
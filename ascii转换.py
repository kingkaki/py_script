#encoding=utf8

string="125-51-95-101-95-48-95-101-117-116-121-108-120-114-110-104-108-51-51-123-110-115"
li=string.split("-")
s=str()
for i in li:
    s+=chr(int(i))
print (s)
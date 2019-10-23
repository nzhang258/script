import os

n=os.listdir('./test')
n.sort()

f1=open('./l.txt','w')
for i in range(len(n)):
	f1.write(n[i]+'\n')
f1.close()

f2=open('./l.txt','r')
lines=f2.readlines()
for ll in lines:
	print(ll[:-1])

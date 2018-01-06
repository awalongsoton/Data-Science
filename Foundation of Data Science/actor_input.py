# -*- coding: utf-8 -*
import os
import pdb
import re
import copy
import csv
import pandas as pd

#header
with open('E:/GitHub/Data_Science/coursework2data/Actor_gross/01.csv') as csvfile:
	reader = csv.reader(csvfile)
	table=[]
	table1=[]
	for row in reader:
		for i in row:
			#pdb.set_trace()
			#print i
			table1.append(re.split('"',i))
			try:
				ii=eval(i)
				table.append(ii)
			except:
				pass
title=[]
content=[]
for name in table1:
	if (table1.index(name) % 2) == 0:	
		title.append(name[0])
title.pop(0)

path = "E:/GitHub/Data_Science/coursework2data/Actor_gross" 
#pdb.set_trace()  
files= os.listdir(path) 
s = []  
temp1=[]
for file in files: 
	
	if not os.path.isdir(file): 
		f = open(path+"/"+file); 
		reader = [row for row in csv.reader(f)] 
		table=[]
		table1=[]
		for row in reader:
			for i in row:
				#pdb.set_trace()
				#print i
				table1.append(re.split('"|$',i))
				try:
					ii=eval(i)
					table.append(ii)
				except:
					pass

		content=[]
		for i in table:
			content.append(i)
		#pdb.set_trace()
		content.pop(0)
		#####spcial process#####
		#####related money
		i_num=[1,3,5]
		#pdb.set_trace()
		for num in i_num:
			for i in content[num]:
				content[num][content[num].index(i)]=content[num][content[num].index(i)].strip('$')
			for i in content[num]:
				content[num][content[num].index(i)]=content[num][content[num].index(i)].replace(',','')		
		#pdb.set_trace()
		for num in i_num:
			for i in content[num]:
				if i.endswith('k')==True:
					content[num][content[num].index(i)]=content[num][content[num].index(i)].strip('k')
				else:
					content[num][content[num].index(i)]=float(content[num][content[num].index(i)])*1000
		#pdb.set_trace()
		#####change str to float
		for num1 in content[2]:
			content[2][content[2].index(num1)]=float(content[2][content[2].index(num1)])
		#####
		content1=copy.deepcopy(content)
		temp=[]
		count=0
		while (count<(len(content1)*len(content1[0]))):
			for i in content:
				#pdb.set_trace()
				temp.append(i[0])
				#pdb.set_trace()
				content[content.index(i)].pop(0)
				count=count+1	
		temp1.append(temp)
temp2=[]
for i in temp1:
	for ii in i:
		temp2.append(ii)
temp3=[temp2[i:i+len(content1)] for i in range(0, len(temp2),len(content1))]

Table_actor = pd.DataFrame(temp3,columns = title).drop_duplicates()
pdb.set_trace()
print Table_actor[:100]
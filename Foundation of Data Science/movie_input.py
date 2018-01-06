# -*- coding: utf-8 -*
import os
import pdb
import re
import copy
import csv
import pandas as pd

#header
with open('E:/GitHub/Data_Science/coursework2data/Movie_detail/1_1.csv') as csvfile:
	reader = csv.reader(csvfile)
	table=[]
	table1=[]
	for row in reader:
		table1.append(row)
title=table1[0]


 
path = "E:/GitHub/Data_Science/coursework2data/Movie_detail" 
#pdb.set_trace()  
files= os.listdir(path) 
s = []  
temp1=[]
content=[]
for file in files: 
	if not os.path.isdir(file): 
		f = open(path+"/"+file); 
		reader = [row for row in csv.reader(f)] 
		table=[]
		for row in reader:
			table.append(row)
		table.pop(0)
		for i in table:
			content.append(i)
#pdb.set_trace()
#####spcial process#####
#####related money
i_num=range(21,28)
#pdb.set_trace()
for num in i_num:
	for i in content:
		content[content.index(i)][num]=content[content.index(i)][num].strip('b')
	for i in content:
		content[content.index(i)][num]=content[content.index(i)][num].strip("'")	
i_num=[19,23,25]
for num in i_num:
	for i in content:
		content[content.index(i)][num]=content[content.index(i)][num].strip('$')
i_num=[15,19,23,24,25,26]
for num in i_num:
	for i in content:
		content[content.index(i)][num]=content[content.index(i)][num].replace(',','')	
i_num=[4]
for num in i_num:		
	for i in content:
		content[content.index(i)][num]=content[content.index(i)][num].rstrip(' min')	
i_num=[1,4,13,14,15,19,23,24,25,26]
for num in i_num:
	for i in content:
		if 	content[content.index(i)][num].isdigit()==True:
			content[content.index(i)][num]=float(content[content.index(i)][num])
		else:
			pass
pdb.set_trace()
Table_actor = pd.DataFrame(content,columns = title).drop_duplicates()
print Table_actor[:10]





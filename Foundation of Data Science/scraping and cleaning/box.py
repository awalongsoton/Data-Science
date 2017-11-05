# coding:utf-8
from urllib import parse
from bs4 import BeautifulSoup
import requests
import re
from functools import wraps
import pandas as pd
import csv
'''
#####################################################################################################
I seperate the url into four parts, the source url, the url before dynamic domain, the dynamic domain
and the field after dynamic domain
Till now, it contains two function, the weekly based office and the actor box office. Firstly, choose
the url,before and after now in order to scrap the data you want.
The first combination of url is the boxoffice weekly
The second combination of url is the boxoffice based on actors
#####################################################################################################
'''
#url='http://www.boxofficemojo.com/weekly/chart/'
#before=None
#after=None

url='http://www.boxofficemojo.com/people/'
before=None
after={'sort':'sumgross','order':'DESC'}



def outer(url,a,b):
    '''
    #########################################################################
    This is the decorator contain parameter used to generate the fixed domain
    #########################################################################
    '''
    def wrappered(fun):
        @wraps(fun)
        def inner(*args,**kwargs):
            for i,change_field in enumerate(fun(*args,**kwargs)):
                if a!=None and b!=None:
                    field_before=parse.urlencode(a)
                    field_after=parse.urlencode(b)
                    yield url+'?'+field_before+'&'+change_field+'&'+field_after
                elif a!=None and b==None:
                    field_before=parse.urlencode(a)
                    yield url+'?'+field_before+'&'+change_field
                elif b!=None and a==None:
                    field_after=parse.urlencode(b)
                    yield url+'?'+change_field+'&'+field_after
                else:
                    yield url+'?'+change_field
        return inner
    return wrappered

#this function used to create the folder in order to store the files
def mkdir(path):
    import os
    path=path.strip()
    path=path.rstrip("\\")
    isExists=os.path.exists(path)
    if not isExists:
        os.makedirs(path)
        return True
    else:
        return False

#decorate the dynamic field
@outer(url,before,after)
def oriurl(field_n1,field_n2,field_v1,field_v2):
    '''
    ###################################################################
    This is used to generate the final url which used to be scraping
    ###################################################################
    '''
    field={}
    for i in field_v1:
        for j in field_v2:
            field[field_n1]=i
            if j<10:
                j='0'+str(j)
            field[field_n2]=j
            field_values = parse.urlencode(field)
            yield field_values
        print('################## All the data of year'+' '+str(i)+' '+'has be collected ##################\n')

def gather(ls,start,step,end):
    s=range(start,end,step)
    result=[ls[i] for i in s]
    return result

def writeCSV(fileName, dataDict):
    '''
    ###################################################################
    Store the data into the csv file
    ###################################################################
    '''
    with open(fileName, "w") as csvFile:
        csvWriter = csv.writer(csvFile)
        for k,v in dataDict.items():
            csvWriter.writerow([k,v])
        csvFile.close()

def generate_info(url,start,end):
    '''
    ########################################################################
    Encapsulate the repeat commands into a function, this function used
    to retrieve the text in the url and return the information after cleaning
    ########################################################################
    '''
    wbdata = requests.get(url).text
    soup = BeautifulSoup(wbdata,'html.parser')
    flag=False
    info=[]
    for ind,s in enumerate(soup.stripped_strings):
        if start==s:
            flag=True
        if flag:
            if s==end:
                break
            else:
                info.append(s)
    try:
        print(info)
    except:
        for inde,ei in enumerate(info):
            try:
                print(ei)
            except:
                info[inde]=ei.encode('utf-8')
    return info

def box_office_weekly():
    '''
    ###########################################################################
    This is the scraping of the box office based on the weekly, firstly, select
    the range of the year and the weeks
    ###########################################################################
    '''
    years=range(2015,2017)
    weeks=range(1,5)
    final_url=oriurl('yr','wk',years,weeks)
    for i in final_url:
        ii=list(i)
        wk=ii[-2:]
        yr=ii[-10:-6]
        info=generate_info(i,'TW','<<Last Week')
        #assert int(info[13])==1
        total=info[-7:]
        info=info[13:len(info)-6]
        head=['Date','TW','LW','Title (Click to view)','Studio','Weekly Gross','Change(%)','Theater Count','Theater Change','Average','Total Gross','Budget*','Week']
        store=dict()
        store[head[0]]=''.join(yr)+'-'+''.join(wk)
        for i in range(0,12):
            store[head[i+1]]=gather(info,i,12,len(info))
        store['Date']=len(store['TW'])*[''.join(yr)+'-'+''.join(wk)]
        filename='Weekly_gross/'+''.join(yr)+'-'+''.join(wk)+'.csv'
        mkdir('Weekly_gross')
        writeCSV(filename,store)

def gross_by_actor():
    '''
    ###########################################################################
    This is the scraping of the box office based on the actors, firstly, select
    the pagenum of the actors, the actors are ranked based on the box office
    ###########################################################################
    '''
    view=['Actor']
    pagenum=range(1,18)
    final_url=oriurl('view','pagenum',view,pagenum)
    filenum=0
    for i in final_url:
        info=generate_info(i,'#801-845','Sort:')
        info=info[1:]
        info=info[9:]
        head=['ROW','Person','Total Gross(Million)','Movie involved','Average Gross for each movie','Most profitbale movie','Gross of most profitable']
        store=dict()
        for i in range(0,7):
            store[head[i]]=gather(info,i,7,len(info))
        filename='Actor_gross/'+str(filenum*50+1)+'-'+str((filenum+1)*50+1)+'.csv'
        mkdir('Actor_gross')
        writeCSV(filename,store)
        filenum=filenum+1

'''
###########################################################################
Run the function you want
###########################################################################
'''
gross_by_actor()

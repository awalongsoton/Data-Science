# coding:utf-8
from urllib import parse
from urllib import request
from collections import defaultdict
from bs4 import BeautifulSoup
import requests
import re
from functools import wraps
import pandas as pd
import csv
import json
import threading
import math
import chardet

'''
#####################################################################################################
I seperate the url into four parts, the source url, the url before dynamic domain, the dynamic domain
and the field after dynamic domain
Till now, it contains three function, the weekly based office, the actor box office and the movie detail. Firstly, choose
the function to scrap and clean the data you want
#####################################################################################################
'''



class BOX_UTIL(object):
    def __init__(self,url,before,after):
        self.url=url
        self.before=before
        self.after=after

        '''
        #########################################################################
        This is the decorator contain parameter used to generate the fixed domain
        #########################################################################
        '''
    def _wrappered(fun):
        @wraps(fun)
        def inner(*args):
            self=args[0]
            for i,change_field in enumerate(fun(*args)):
                if self.before!=None and self.after!=None:
                    field_before=parse.urlencode(self.before)
                    field_after=parse.urlencode(self.after)
                    yield self.url+'?'+field_before+'&'+change_field+'&'+field_after
                elif self.before!=None and self.after==None:
                    field_before=parse.urlencode(self.before)
                    yield self.url+'?'+field_before+'&'+change_field
                elif self.after!=None and self.before==None:
                    field_after=parse.urlencode(self.after)
                    yield self.url+'?'+change_field+'&'+field_after
                else:
                    yield self.url+'?'+change_field
        return inner


    #this function used to create the folder in order to store the files
    def mkdir(self,path):
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
    @_wrappered
    def oriurl(self,field_n1,field_n2,field_v1,field_v2):
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

    def gather(self,ls,start,step,end):
        s=range(start,end,step)
        result=[ls[i] for i in s]
        return result

    def writeCSV(self,fileName, dataDict):
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

    def generate_info(self,url,start,end):
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
                    info.append(s.encode('utf-8'))
        '''
        try:
            print(info)
        except:
            for inde,ei in enumerate(info):
                try:
                    print(ei)
                except:
                    print('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
                    print(chardet.detect(ei))
                    print('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
                    info[inde]=ei.encode('utf-8')
        '''
        return info

def get_url_list():
    '''
    #############################################################################################
    the function extract the url frin box office mojo website which contain nearly all the movies
    #############################################################################################
    '''
    url_list=[]
    seed_url='http://www.boxofficemojo.com/movies/alphabetical.htm?letter=B&p=.htm'
    alpha_url=[]
    html=request.urlopen(seed_url).read().decode('utf-8').strip()
    webpage_regex=re.compile('<a[^>]+href=["\'](.*?)["\']',re.IGNORECASE)
    for i in webpage_regex.findall(html):
        #print(i)
        if re.match(r'/movies/alphabetical\.htm\?letter=[A-Z]&p=\.htm', str(i)):
            #print(i)
            alpha_url.append(i)
    alpha_url=list(set(alpha_url))
    source_url='http://www.boxofficemojo.com'
    while alpha_url:
        second_url=alpha_url.pop()
        page_url=[]
        ss=re.compile(r'[A-Z]')
        cap=ss.findall(second_url)
        if cap==['R']:
            #print('yes')
            for s in range(2,7):
                url_list.append(source_url+'/movies/alphabetical.htm?letter=R&page='+str(s)+'&p=.htm')
            continue
        #print(source_url+second_url)
        try:
            html=request.urlopen(source_url+second_url).read().decode('utf-8').strip()
        except:
            try:
                html=request.urlopen(source_url+second_url).read().decode('gb2312').strip()
                print(html)
            except:
                print('########################################################################')
        webpage_regex=re.compile('<a[^>]+href=["\'](.*?)["\']',re.IGNORECASE)
        for i in webpage_regex.findall(html):
            if re.match(r'/movies/alphabetical\.htm\?letter=%s&page=[0-9]&p=\.htm'%(cap), str(i)):
                url_list.append(source_url+i)
    url_list.append('http://www.boxofficemojo.com/movies/alphabetical.htm?letter=NUM&p=.htm')
    return list(set(url_list))


def box_office_weekly():
    '''
    ###########################################################################
    This is the scraping of the box office based on the weekly, firstly, select
    the range of the year and the weeks
    ###########################################################################
    '''
    util=BOX_UTIL('http://www.boxofficemojo.com/weekly/chart/',None,None)
    years=range(2007,2018)
    weeks=range(1,53)
    final_url=util.oriurl('yr','wk',years,weeks)
    for i in final_url:
        ii=list(i)
        wk=ii[-2:]
        yr=ii[-10:-6]
        info=util.generate_info(i,'TW','<<Last Week')
        #assert int(info[13])==1
        total=info[-7:]
        info=info[13:len(info)-6]
        head=['Date','TW','LW','Title (Click to view)','Studio','Weekly Gross','Change(%)','Theater Count','Theater Change','Average','Total Gross','Budget(Million)','Week']
        store=dict()
        store[head[0]]=''.join(yr)+'-'+''.join(wk)
        for i in range(0,12):
            store[head[i+1]]=util.gather(info,i,12,len(info))
        store['Date']=len(store['TW'])*[''.join(yr)+'-'+''.join(wk)]
        filename='Weekly_gross/'+''.join(yr)+'-'+''.join(wk)+'.csv'
        util.mkdir('Weekly_gross')
        util.writeCSV(filename,store)



def gross_by_actor():
    '''
    ###########################################################################
    This is the scraping of the box office based on the actors, firstly, select
    the pagenum of the actors, the actors are ranked based on the box office
    ###########################################################################
    '''
    view=['Actor']
    pagenum=range(1,18)
    util=BOX_UTIL('http://www.boxofficemojo.com/people/',None,{'sort':'sumgross','order':'DESC'})
    final_url=util.oriurl('view','pagenum',view,pagenum)
    filenum=0
    for i in final_url:
        info=util.generate_info(i,'#801-848','Sort:')
        info=info[1:]
        info=info[9:]
        head=['ROW','Person','Total Gross(Million)','Movie involved','Average Gross for each movie','Most profitbale movie','Gross of most profitable']
        store=dict()
        for i in range(0,7):
            store[head[i]]=util.gather(info,i,7,len(info))
        filename='Actor_gross/'+str(filenum*50+1)+'-'+str((filenum+1)*50+1)+'.csv'
        util.mkdir('Actor_gross')
        util.writeCSV(filename,store)
        filenum=filenum+1

def gross_by_director():
    '''
    ###########################################################################
    This is the scraping of the box office based on the directors, firstly, select
    the pagenum of the directors, the directors are ranked based on the box office
    ###########################################################################
    '''
    view=['Actor']
    pagenum=range(1,18)
    util=BOX_UTIL('http://www.boxofficemojo.com/people/',None,{'view':'Director','sort':'sumgross','order':'DESC'})
    final_url=util.oriurl('view','pagenum',view,pagenum)
    filenum=0
    for i in final_url:
        info=util.generate_info(i,'#851-885','Sort:')
        info=info[1:]
        info=info[9:]
        head=['ROW','Person','Total Gross(Million)','Movie involved','Average Gross for each movie','Most profitbale movie','Gross of most profitable']
        store=dict()
        for i in range(0,7):
            store[head[i]]=util.gather(info,i,7,len(info))
        filename='Director_gross/'+str(filenum*50+1)+'-'+str((filenum+1)*50+1)+'.csv'
        util.mkdir('Director_gross')
        util.writeCSV(filename,store)
        filenum=filenum+1

def movie_detail(index,url_list=[]):
    '''
    #############################################################################
    The function query the omdb websites for the detail of each movie and connect
    the two tables
    #############################################################################
    '''
    #print('########################## All the urls have been generated ########################### ')
    iii=0
    while url_list:
        iii=iii+1
        #print('=======================================the '+str(iii)+' url===============================\n')
        url=url_list.pop()
        stupid_url=['http://www.boxofficemojo.com/movies/alphabetical.htm?letter=T&page=5&p=.htm','http://www.boxofficemojo.com/movies/alphabetical.htm?letter=P&page=7&p=.htm','http://www.boxofficemojo.com/movies/alphabetical.htm?letter=F&page=2&p=.htm']
        if url in stupid_url:
            continue
        print(url)
        util=BOX_UTIL(url,None,None)
        info=util.generate_info(url,'Open','Key: * = multiple releases.  n/a = information is not available.')
        info=info[1:]
        head=['Title','Studio','Total Gross','Theaters','Opening Gross','Theaters(opening)','Open']
        store=dict()
        movie_list=list()
        for i in range(0,7):
            store[head[i]]=util.gather(info,i,7,len(info))
        #print('############finish to scrapy, next step is to query the movie detail##############')
        for ind,i in enumerate(store['Title']):
            try:
                yr=str(store['Open'][ind])
            except:
                print(url)
                print(store)
                print(1/0)
            x=lambda yr:yr[-4:] if yr!='TBD' and yr!='N/A' else None
            if x(yr)==None:
                result_dic=omdb_api(i,None)
            else:
                result_dic=omdb_api(i,x(yr))
            if result_dic==None:
                continue
            del result_dic['Poster']
            del result_dic['Plot']
            del result_dic['Response']
            for j in range(1,7):
                result_dic[head[j]]=store[head[j]][ind]
            movie_list.append(result_dic)
            if ind%50==0:
                print('#############thread '+str(index)+' finish query '+str(ind)+'amount of data##############################')
        util.mkdir('Movie_detail')
        filename='Movie_detail/'+str(index)+'_'+str(iii)+'.csv'
        headers=['Title','Year','Rated','Released','Runtime','Genre','Director','Writer','Actors','Language','Country','Awards','Ratings','Metascore','imdbRating','imdbVotes','imdbID','Type','DVD','BoxOffice','Production','Website','Studio','Total Gross','Theaters','Opening Gross','Theaters(opening)','Open']
        write_dic_csv(filename,headers,movie_list)

def thread_extracting():
    '''
    ###########################################################################
    Using thread to make the querying much faster
    ###########################################################################
    '''
    threads_list=list()
    url_list=get_url_list()
    length=len(url_list)
    total_thread=13
    step=math.floor(length/total_thread)
    for i in range(1,total_thread+1):
        if i==total_thread:
            threadi=threading.Thread(target = movie_detail, args=(i,url_list[(i-1)*step:],), name = 'thread-' + str(i))
        else:
            threadi=threading.Thread(target = movie_detail, args=(i,url_list[(i-1)*step:i*step],), name = 'thread-' + str(i))
        threads_list.append(threadi)
        threadi.start()
    for thi in threads_list:
        thi.join()


def omdb_api(name,year):
    '''
    ###########################################################################
    Invoking the API of OMDB
    ###########################################################################
    '''
    ori_url='http://www.omdbapi.com/?'
    if year!=None:
        after=parse.urlencode({'t':name,'y':str(year),'apikey':'82c7e8a7'})
    else:
        after=parse.urlencode({'t':name,'apikey':'82c7e8a7'})
    url=ori_url+str(after)
    try:
        response = requests.get(url)
        attr_dict = json.loads(response.text)
    except:
        return None
    if attr_dict['Response']=='False':
        return None
    return attr_dict

def write_dic_csv(filename,headers,dic):
    '''
    ###########################################################################
    Writing list of dictionary to CSV
    ###########################################################################
    '''
    with open(filename, "w",encoding= 'utf8') as csvFile:
        csvWriter=csv.DictWriter(csvFile, headers,extrasaction='ignore')
        csvWriter.writeheader()
        csvWriter.writerows(dic)
        csvFile.close()



'''
###########################################################################
Run the function you want
###########################################################################
'''
#thread_extracting()
#box_office_weekly()
gross_by_director()
#gross_by_actor()

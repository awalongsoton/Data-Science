#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 20 12:00:06 2017

@author: chenqiling
"""

'''
#################
Connect to Google
#################
'''

from pytrends.request import TrendReq

# Login to Google. Only need to run this once, the rest of requests will use the same session.
pytrends = TrendReq()


'''
################################################################
Build Payload, and timeframe represents the date to start from ,
we can use this to know the different periods,cat=category,cat（Defaults to no category）
geo=two letter country abbreviation（Defaults to World）,gprop represent google 
property to filter to（Defaults to web searches）
################################################################
'''

kw_list = ["samuel jackson"]
#pytrend.build_payload(kw_list=['ROW','Person','Total Gross(Million)],cat=34,timeframe='today 5-y')



# Create payload and capture API tokens. Only needed for interest_over_time(), interest_by_region() & related_queries()
a=pytrends.build_payload(kw_list)

# Interest Over Time
interest_over_time_df = pytrends.interest_over_time()
print(interest_over_time_df.head())




# Interest by Region
interest_by_region_df = pytrends.interest_by_region(resolution='COUNTRY')
print(interest_by_region_df.head())

# Related Queries, returns a dictionary of dataframes
related_queries_dict = pytrends.related_queries()
print(related_queries_dict)

# Get Google Hot Trends data
trending_searches_df = pytrends.trending_searches()
print(trending_searches_df.head())

# Get Google Top Charts
top_charts_df = pytrends.top_charts(cid='Movie_actor',date=201612)
print(top_charts_df.head())

# Get Google Keyword Suggestions
suggestions_dict = pytrends.suggestions(keyword='samuel jackson')
print(suggestions_dict)

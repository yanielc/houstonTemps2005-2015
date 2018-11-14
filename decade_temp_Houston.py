#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Oct 21 20:31:17 2018

@author: cabrera
"""


'''1. Read the documentation and familiarize yourself with the dataset, then write some
    by day of the year over the period 2005-2014. The area between the record high and record low temperatures for each day should
    be shaded.
    
    2. Overlay a scatter of the 2015 data for any points (highs and lows) for 
    which the ten year record (2005-2014) record high or record low was broken in 2015.'''
 
 
import pandas as pd, numpy as np
import matplotlib.pyplot as plt

def read_file():
   
    # function to read in data
    
    df = pd.read_csv('weather.csv')
    df2015 = df[df['Date'] > '2014-12-31']   # data for 2015 only
    df2015.loc[:,'Data_Value'] = df2015['Data_Value']/10 # convert to Celcius
    df = df[df['Date'] < '2015-01-01']           # data for 2005-2014
    df.loc[:,'Data_Value'] = df['Data_Value']/10 # convert to Celcius
    
    return df, df2015
   
def record_lines():
   
    df, df2015 = read_file()
    
    #remove feb 29th from dataset (allowed for visualization)
    df = df.drop(df[df['Date'].isin(['2008-04-29','2012-04-29'])].index)
    
    
    # max and min temps for range of years 2005-2014
    tmax_df = df[df['Element'] == 'TMAX'].groupby('Date').mean().reset_index()  # get mean for each day since we have multiple recordings
    tmin_df = df[df['Element'] == 'TMIN'].groupby('Date').mean().reset_index()
    
    # group by day of the year
    tmax_df['mod365'] = pd.DataFrame([x % 365 for x in tmax_df.index.tolist()], index= tmax_df.index)
    tmin_df['mod365'] = pd.DataFrame([x % 365 for x in tmin_df.index.tolist()], index= tmin_df.index)
     
    
    # create df for latest year 2015, and add extrema from range of years 2005-2014
    t2015max_df = df2015[df2015['Element'] == 'TMAX'].groupby('Date').mean().reset_index()
    t2015max_df['2005-2014_highest'] = tmax_df.groupby('mod365').max()['Data_Value']
    
    t2015min_df = df2015[df2015['Element'] == 'TMIN'].groupby('Date').mean().reset_index()
    t2015min_df['2005-2014_lowest'] = tmin_df.groupby('mod365').min()['Data_Value']
    
    print(t2015max_df.head())
    # create column containing only those values from 2015 when the records were broken
    t2015max_df['record_in_2015'] = pd.DataFrame(t2015max_df[t2015max_df['Data_Value'] == t2015max_df[['Data_Value', '2005-2014_highest']].max(axis=1) ]['Data_Value'], index= t2015max_df.index)
    t2015min_df['record_in_2015'] = pd.DataFrame(t2015min_df[t2015min_df['Data_Value'] == t2015min_df[['Data_Value','2005-2014_lowest']].min(axis=1)]['Data_Value'], index= t2015min_df.index)
   
    
    
    #graphs for range of years 2005-2014
    plt.figure(figsize=(12,8))
    plt.title('2005-2014 max and min daily temperature records. Records broken in 2015.')
    plt.plot(t2015max_df['Date'],t2015max_df['2005-2014_highest'],'-r',linewidth=1,label='2005-2014 highest record')
    plt.plot(t2015min_df['Date'],t2015min_df['2005-2014_lowest'],'-b',linewidth=1, label='2005-2014 lowest record')
    plt.xticks(np.arange(1,len(t2015max_df),33), ('Jan', 'Feb', 'Mar', 'Apr', 'May','Jun','Jul','Aug','Sep','Oct','Nov', 'Dec'))
    plt.gca().fill_between(t2015max_df['Date'], t2015min_df['2005-2014_lowest'], t2015max_df['2005-2014_highest'],facecolor='green',
           alpha=0.1)
     
    
    # plot records broken in 2015
    plt.plot(t2015max_df['Date'], t2015max_df['record_in_2015'], '*', color = 'purple', label = 'max temp broken in 2015')
    plt.plot(t2015min_df['Date'], t2015min_df['record_in_2015'], '*', color='orange', label = 'min temp broken in 2015')
   
    plt.legend(frameon=False)
    plt.xlabel('Days')
    plt.ylabel('Temperature °C')
    plt.savefig('daily_temps_and_broken_records.png')


    
    
    
if __name__ == '__main__':
    
    record_lines()
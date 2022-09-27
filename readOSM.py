#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep  7 20:17:59 2022

@author: joe
"""


import json
import pandas as pd
import xmltodict

#

templateDF = pd.DataFrame({
    "id":[], 
    "created_at":[], 
    "closed_at":[],
    "open":[],
    "user":[],
    "uid":[],
    "min_lat":[], 
    "min_lon":[], 
    "max_lat":[],
    "max_lon":[],
    "num_changes":[],
    "comments_count":[]
    })

columns = ["id",
           "created_at",
           "closed_at",
           "open",
           "user",
           "uid",
           "min_lat",
           "min_lon",
           "max_lat",
           "max_lon",
           "num_changes",
           "comments_count"]

#

i = 0
j = 0
df = templateDF
with open("changesets-220829.osm") as fp:
    while i < 772000000:
        
        while j < 100000:
            line = fp.readline()
            #print(line)
            if line.startswith(' <changeset '):
                try:
                    line = line.replace(' <changeset ','"')
                    line = line.replace('/>','')
                    line = line.replace('>','')
                    line = line.replace('=','":[')
                    line = line.replace('" ','"], "')
                    line = '{' + line + ']}'
                    #print(line)
                    lineDict = json.loads(line)
                    #print(lineDict)
                    lineDF = pd.DataFrame(lineDict)
                    df = pd.concat([df,lineDF])
                    df = df[columns]
                    if i%100 == 0:
                        print(i," ",j)
                    i += 1
                    j += 1
                except:
                    print('error thrown, continuing on')
        
        labelnumber = int(i/100000)
        
        if labelnumber >= 0 and labelnumber < 10:
            labelnumber = '000{}'.format(labelnumber)
        elif labelnumber >= 10 and labelnumber < 100:
            labelnumber = '00{}'.format(labelnumber)
        elif labelnumber >= 100 and labelnumber < 1000:
            labelnumber = '0{}'.format(labelnumber)
        elif labelnumber >= 1000 and labelnumber < 10000:
            labelnumber = '{}'.format(labelnumber)
        else:
            print('error')
        
        df.to_csv('csv_out/osm_{}.csv'.format(labelnumber))
        df = templateDF
        j = 0
        


       
        
        


    
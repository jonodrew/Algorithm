import pandas as pd
import numpy as np
from collections import Counter
import random

def swapFunc(df1, df2):
    df1 = reindex(df1) #to make sure the random number is in the index
    df2 = reindex(df2) #ditto
    rand1 = random.randrange(0,len(df1)) #generates random number for df1 list
    rand2 = random.randrange(0,len(df2)) #ditto for leftover df2
    df2 = df2.append(df1.ix[rand1]) #adds random row from df1 to df2
    df1 = df1.drop(rand1) #deletes that  row from df1 table
    df1 = df1.append(df2.ix[rand2]) #appends random row from df2 table
    df2 = df2.drop(rand2) #deletes that row from df2
    return df1,df2,rand1,rand2

def swapBack(df1,df2,int1,int2):
    df2 = df2.append(df1.ix[int2]) #adds random row from df1 to df2
    df1 = df1.drop(int2) #deletes that  row from df1 table
    df1 = df1.append(df2.ix[int1]) #appends random row from df2 table
    df2 = df2.drop(int1) #deletes that row from df2
    return df1,df2

def dayCalc(df):
    day1 = df['Day 1'].value_counts()
    day2 = df['Day 2'].value_counts()
    #print(day1.ix[1], day2.ix[1])
    if day1.ix[1] >= 250 and day2.ix[1] >= 250:
        dayMetric = True
    else:
        dayMetric = False
    #print (dayMetric)
    return dayMetric
def regionCalc(df):
    regionDict = dict(Counter(" ".join(df['Region'].values.tolist()).split(" ")).items())
    for region in regionDict:
        regionDict[region] = float(regionDict.get(region))/len(df)

    if regionDict.get('OOL') >= .24 and regionDict.get('OOL') <= .26:
        oolMetric = True
    else:
        oolMetric = False
    if regionDict.get('London') >= .74 and regionDict.get('London') <= .76:
        londonMetric = True
    else:
        londonMetric = False
    if londonMetric == True and oolMetric == True and (
    regionDict.get('London')+regionDict.get('OOL') == 1.0):
        regionMetric = True
    else:
        regionMetric = False
    return regionMetric
def streamCalc(df):
    streamDict = dict(Counter(" ".join(delegates['CSR'].values.tolist()).split(" ")).items())
    CSR_metric = False
    non_CSR_metric = False
    FT_metric = False
    for stream in streamDict:
        streamDict[stream] = int(streamDict.get(stream))
    #print(streamDict)
    if streamDict.get('CSR') >= 310 and streamDict.get('CSR') <= 370:
        CSR_metric = True
    if streamDict.get('non-CSR') >= 60 and streamDict.get('non-CSR') <= 120:
        non_CSR_metric = True
    if streamDict.get('FT') >= 20 and streamDict.get('FT') <= 70:
        FT_metric = True
    if CSR_metric == True and non_CSR_metric == True and FT_metric == True:
        streamMetric = True
    else:
        streamMetric = False
    #print(streamDict)
    return streamMetric
def reindex(df):
    newIndex = range(0,len(df))
    df['Index'] = newIndex
    df = df.set_index('Index')
    return df
max_iterations = 5000
metrics = {}
stream_targets = {'CSR':350,'non-CSR':100,'FT':50}
for i in range(1):
    print("Begin test %d" % (i+1))
    success = False
    iteration = 0
    while success == False:
        print("Start attempt number: %d" % (iteration+1))
        if iteration > 99:
            break
        applicants = pd.read_csv('test.csv')
        rows = random.sample(applicants.index, 500)
        delegates = applicants.ix[rows]
        applicants = applicants.drop(rows)
        dayMetric = dayCalc(delegates)
        regionMetric = regionCalc(delegates)
        streamMetric = streamCalc(delegates)
        stream_loop = 0
        while streamMetric == False:
            region_loop = 0
            while regionMetric == False:
                day_loop = 0
                while dayMetric == False:
                    #print('Started day loop')
                    pre_day1 = 0
                    pre_day1 = delegates['Day 1'].value_counts().ix[1]
                    dataframes = swapFunc(delegates,applicants)
                    delegates = dataframes[0]
                    applicants = dataframes[1]
                    post_day1 = delegates['Day 1'].value_counts().ix[1]
                    if abs(250 - post_day1) > abs(250 - pre_day1):
                        dataframes = swapBack(delegates,applicants,dataframes[2],dataframes[3])
                        delegates = dataframes[0]
                        applicants = dataframes[1]
                    regionMetric = regionCalc(delegates)
                    dayMetric = dayCalc(delegates)
                    streamMetric = streamCalc(delegates)
                    day_loop += 1
                    #print('This is the end of day loop %d' % day_loop)
                    if day_loop > max_iterations:
                        break
                #print('Started region loop')
                dataframes = swapFunc(delegates,applicants)
                delegates = dataframes[0]
                applicants = dataframes[1]
                #print('Swapping regional candidate')
                regionMetric = regionCalc(delegates)
                dayMetric = dayCalc(delegates)
                streamMetric = streamCalc(delegates)
                region_loop += 1
                #print('This is the end of region loop %d' % region_loop)
                if region_loop > max_iterations:
                    break
            #print('Started stream loop')
            dataframes = swapFunc(delegates,applicants)
            delegates = dataframes[0]
            applicants = dataframes[1]
            #print('Swapping stream candidate')
            streamMetric = streamCalc(delegates)
            post_stream = dict(Counter(" ".join(delegates['CSR'].values.tolist()).split(" ")).items())
            for k in post_stream:
                if post_stream[k] > stream_targets[k]:
                    swapBack(delegates,applicants, dataframes[2],dataframes[3])
                    stream_loop +=1
                    break
            regionMetric = regionCalc(delegates)
            dayMetric = dayCalc(delegates)
            stream_loop +=1
            #print('This is the end of stream loop %d' % stream_loop)
            if stream_loop > max_iterations:
                break
        a = regionCalc(delegates)
        b = streamCalc(delegates)
        c = dayCalc(delegates)
        if a == True and b == True and c == True:
            print("Success! Delegate list compiled")
            iteration += 1
            #success = True
            result = [a,b,c]
            metrics[iteration] = a,b,c
            day_1 = pd.DataFrame(columns = delegates.columns)
            day_2 = pd.DataFrame(columns = delegates.columns)
            reserves_df = pd.DataFrame(columns = delegates.columns)
            for index, row in delegates.iterrows():
                if row['Day 1'] == 1 and len(day_1.index) <= 250:
                    day_1.append(delegates.ix[row])
                elif row['Day 2'] == 1 and len(day_2.index) <= 250:
                    day_2.append(delegates.ix[row])
                else:
                    reserves_df.append(delegates.ix[row])
            day_1.to_csv('results/day_1_%d.csv' % i)
            day_2.to_csv('results/day_2_%d.csv' % i)
            reserves_df.to_csv('results/reserves_%d.csv' % i)
        else:
            iteration += 1
            print("Attempt %d unsuccessful!" % iteration)
            result = [a,b,c]
            metrics[iteration] = a,b,c
print(metrics)

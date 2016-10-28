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
    return df1,df2

def dayCalc(df):
    day1 = df['Day 1'].value_counts()
    day2 = df['Day 2'].value_counts()
    if day1.ix[1] > 250 and day2.ix[1] > 250:
        dayMetric = True
    else:
        dayMetric = False
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
        streamDict[stream] = float(streamDict.get(stream))/len(df)
    #print(streamDict)
    if streamDict.get('CSR') >= 0.65 and streamDict.get('CSR') <= 0.72:
        CSR_metric = True
    if streamDict.get('non-CSR') >= 0.18 and streamDict.get('non-CSR') <= 0.29:
        non_CSR_metric = True
    if streamDict.get('FT') >= 0.03 and streamDict.get('FT') <= 0.12:
        FT_metric = True
    if CSR_metric == True and non_CSR_metric == True and FT_metric == True and (
    streamDict.get('CSR') + streamDict.get('non-CSR') + streamDict.get('FT') ==
    1.0):
        streamMetric = True
    else:
        streamMetric = False
    return streamMetric

def reindex(df):
    newIndex = range(0,len(df))
    df['Index'] = newIndex
    df = df.set_index('Index')
    return df

max_iterations = 10000
metrics = {}
for i in range(100):
    print("This is round %d" % i)
    success = False
    iteration = 0
    while success == False:
        if iteration > 1000:
            break
        applicants = pd.read_csv('test.csv')
        rows = random.sample(applicants.index, 800)
        delegates = applicants.ix[rows]
        applicants = applicants.drop(rows)
        day_loop = 1
        region_loop = 1
        stream_loop = 1
        dayMetric = False
        regionMetric = False
        streamMetric = False
        while streamMetric == False:
            while regionMetric == False:
                while dayMetric == False:
                    print('Started day loop')
                    dataframes = swapFunc(delegates,applicants)
                    delegates = dataframes[0]
                    applicants = dataframes[1]
                    #print('This is the end of day loop %d' % day_loop)
                    day_loop +=1
                    dayMetric = dayCalc(delegates)
                print('Started region loop')
                dataframes = swapFunc(delegates,applicants)
                delegates = dataframes[0]
                applicants = dataframes[1]
                #print('Swapping regional candidate')
                regionMetric = regionCalc(delegates)
                dayMetric = dayCalc(delegates)
                region_loop +=1
                if region_loop > 100:
                    break
                break
                #print('This is the end of region loop %d' % region_loop)
            print('Started stream loop')
            dataframes = swapFunc(delegates,applicants)
            delegates = dataframes[0]
            applicants = dataframes[1]
            #print('Swapping stream candidate')
            streamMetric = streamCalc(delegates)
            stream_loop +=1
            #print('This is the end of stream loop %d' % stream_loop)
            if stream_loop > 100:
                break
            if streamMetric == True and regionMetric == True and dayMetric == True:
                print("Delegate list compiled")
                success = True
                a = regionCalc(delegates)
                b = streamCalc(delegates)
                c = dayCalc(delegates)
                result = [a,b,c]
                metrics[i] = a,b,c
                day_1 = pd.DataFrame(columns = delegates.columns)
                day_2 = pd.DataFrame(columns = delegates.columns)
                reserves_df = pd.DataFrame(columns = delegates.columns)
                for index, row in delegates.iterrows():
                    if row['Day 1'] == 1 and len(day_1.index) < 250:
                        day_1.loc[index] = row
                    elif row['Day 2'] == 1 and len(day_2.index) < 250:
                        day_2.loc[index] = row
                    else:
                        reserves_df.loc[index] = row
                day_1.to_csv('results/day_1_%d.csv' % i)
                day_2.to_csv('results/day_2_%d.csv' % i)
                reserves_df.to_csv('results/reserves_%d.csv' % i)
            else:
                iteration += 1
                print("This is the end of iteration %d" % iteration)
                break



print(metrics)

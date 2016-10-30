import pandas as pd
import numpy as np
from collections import Counter
import random
import time
import sys

times = {}
metrics = {}
success = False
test1 = createData()
max_iterations = 2500
tickets_available = 500
regions = ['OOL','London']
streams = ['CSR','non-CSR','FT']
cols = ['ID','Region','Stream','Day 1','Day 2']
stream_targets = {'CSR':350,'non-CSR':100,'FT':50}
metrics = pd.DataFrame(columns = ['Attempt','Day','Region','Stream'])

def createData():
    """this function creates 2000 rows of random data according to the constraints
    set out below. They can be editted for harder testing"""
    df = []
    for i in range(2000):
        r = [i]
        rand1 = random.random()
        rand2 = random.random()
        rand3 = random.randrange(1,3)
        if rand1 > 0.75:
            r.append(regions[0])
        else:
            r.append(regions[1])
        if rand2 < 0.70:
            r.append(streams[0])
        elif rand2 < 0.90:
            r.append(streams[1])
        else:
            r.append(streams[2])
        if rand3 == 1:
            r.append(1)
            r.append(0)
        elif rand3 == 2:
            r.append(0)
            r.append(1)
        else:
            r.append(1)
            r.append(1)
        df.append(r)
    df = pd.DataFrame(df,columns=cols)
    return df
def swapFunc(df1, df2):
    """This function swaps two random rows from the delegates dataframe to the
    applicants dataframe"""
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
    """Does what it says on the tin"""
    df2 = df2.append(df1.ix[int2]) #adds random row from df1 to df2
    df1 = df1.drop(int2) #deletes that  row from df1 table
    df1 = df1.append(df2.ix[int1]) #appends random row from df2 table
    df2 = df2.drop(int1) #deletes that row from df2
    return df1,df2
def dayCalc(df):
    """This calculates whether there are 250 attendees per day"""
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
    """Calculates whether the regions are in the ratios below AND if the day metric
    is still correct"""
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
    if bool(londonMetric * oolMetric) == True and (
    regionDict.get('London')+regionDict.get('OOL') == 1.0):
        regionMetric = True
    else:
        regionMetric = False
    return regionMetric
def streamCalc(df):
    streamDict = dict(Counter(" ".join(delegates['Stream'].values.tolist()).split(" ")).items())
    CSR_metric = False
    non_CSR_metric = False
    FT_metric = False
    for stream in streamDict:
        streamDict[stream] = int(streamDict.get(stream))
    #print(streamDict)
    if streamDict.get('CSR') >= 340 and streamDict.get('CSR') <= 360:
        CSR_metric = True
    if streamDict.get('non-CSR') >= 90 and streamDict.get('non-CSR') <= 110:
        non_CSR_metric = True
    if streamDict.get('FT') >= 40 and streamDict.get('FT') <= 60:
        FT_metric = True
    if bool(CSR_metric * non_CSR_metric * FT_metric) == True:
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
def successCalc(df):
    a = regionCalc(df)
    b = streamCalc(df)
    c = dayCalc(df)
    a = bool(a * c)
    b = bool(a * b * c)
    successMetric = bool(a * b * c)
    #print("Day correct: %s \nRegion correct: %s \nStream correct: %s \n" % (c,a,b))
    return successMetric,a,b,c
for j in range(100):
    start_time = time.time()
    success = False
    iteration = 0
    while success == False:
        attempt = "%d.%d" % (j,iteration)
        if iteration > 99:
            break
        start_iteration_time = time.time()
        print("Attempt: %d.%d" % (j,iteration))
        applicants = test1
        rows = random.sample(applicants.index, tickets_available)
        delegates = applicants.ix[rows]
        applicants = applicants.drop(rows)
        success_outputs = successCalc(delegates)
        success = success_outputs[0]
        regionMetric = False
        dayMetric = False
        streamMetric = False
        stream_loop = 0
        while streamMetric == False:
            region_loop = 0
            while regionMetric == False:
                day_loop = 0
                while dayMetric == False:
                    success_outputs = successCalc(delegates)
                    success = success_outputs[0]
                    regionMetric = success_outputs[1]
                    streamMetric = success_outputs[2]
                    dayMetric = success_outputs[3]
                    if dayMetric == True:
                        break
                    pre_day1 = delegates['Day 1'].value_counts().ix[1]
                    dataframes = swapFunc(delegates,applicants)
                    delegates = dataframes[0]
                    applicants = dataframes[1]
                    post_day1 = delegates['Day 1'].value_counts().ix[1]
                    if abs(250 - post_day1) > abs(250 - pre_day1):
                        dataframes = swapBack(delegates,applicants,dataframes[2],dataframes[3])
                        delegates = dataframes[0]
                        applicants = dataframes[1]
                    day_loop += 1
                    dayMetric = dayCalc(delegates)
                    if day_loop > max_iterations:
                        break
                if regionMetric == True:
                    break
                dataframes = swapFunc(delegates,applicants)
                delegates = dataframes[0]
                applicants = dataframes[1]
                success_outputs = successCalc(delegates)
                region_loop += 1
                if region_loop > max_iterations:
                    break
                dayMetric = success_outputs[3]
                regionMetric = success_outputs[1]
            if streamMetric == True:
                break
            dataframes = swapFunc(delegates,applicants)
            delegates = dataframes[0]
            applicants = dataframes[1]
            post_stream = dict(Counter(" ".join(delegates['Stream'].values.tolist()).split(" ")).items())
            for k in post_stream:
                if post_stream[k] > stream_targets[k]:
                    swapBack(delegates,applicants, dataframes[2],dataframes[3])
                    stream_loop +=1
                    break
                break
            success_outputs = successCalc(delegates)
            success = success_outputs[0]
            regionMetric = success_outputs[1]
            dayMetric = success_outputs[3]
            streamMetric = success_outputs[2]
            stream_loop +=1
            if stream_loop > max_iterations:
                metrics.loc[attempt] = [attempt,dayMetric,regionMetric,streamMetric]
                iteration += 1
                print("Fail")
                success = False
                break
    if success == True:
        metrics.loc[attempt] = [attempt,dayMetric,regionMetric,streamMetric]
        print("Success! Delegate list compiled")
        day_1 = pd.DataFrame(columns = delegates.columns)
        day_2 = day_1
        reserves_df = day_1
        for index,row in delegates.iterrows():
            if row['Day 1'] == 1 and len(day_1.index) < 250:
                day_1 = day_1.append(delegates.ix[index])
            elif row['Day 2'] == 1 and len(day_2.index) < 250:
                day_2.append(delegates.ix[index])
            else:
                reserves_df.append(delegates.ix[row])
        day_1.to_csv('results/day1_iteration%d.%d.csv' % (j,iteration))
        day_2.to_csv('results/day2_iteration%d.%d.csv' % (j,iteration))
        reserves_df.to_csv('results/reserves_iteration%d.%d.csv' % (j,iteration))
    else:
        metrics.loc[attempt] = [attempt,dayMetric,regionMetric,streamMetric]
        iteration += 1
        print("No solutions found. Trying next dataset")
    end_time = (time.time()-start_time)/60
    times[j] = end_time
    test1 = createData()
    print("New data")
print("Test complete")
times = pd.DataFrame(times.items(),columns = ['Attempt','Time (m)'])
times.to_csv('results/times.csv')

import pandas as pd
import numpy as np
from collections import Counter
import random
import time
import sys

times = {}
metrics = {}
success = False
max_iterations = 9999
max_attempts = 99
tickets_available = 500
regions = ['SE','SW','NW','NE','Scotland','Anglia','Wales','Yorkshire','Midlands']
region_target = {'London':.751,"SE":0.037,'SW':0.026,'Wales':0.039,
'Anglia':0.004,'Midlands':0.005,'Yorkshire':0.048,'NW':0.023,'NE':0.017,
'Scotland':0.041}
streams = ['CSR','non-CSR','FT']
cols = ['ID','Region','Stream','Day 1','Day 2']
stream_target = {'CSR':350,'non-CSR':100,'FT':50}
metrics = pd.DataFrame(columns = ['Attempt','Day','Region','Stream'])
def createData():
    """this function creates rows of random data according to the constraints
    set out below. They can be editted for harder testing"""
    df = []
    this_test_numbers = []
    applicants_number = random.randrange(8,25)*100
    for i in range(applicants_number):
        r = [i]
        rand1 = random.random()
        rand2 = random.random()
        rand3 = random.randrange(1,3)
        London_bound = random.uniform(0.65,0.85)
        csr_bound = random.uniform(0.6,0.8)
        ncsr_bound = random.uniform(0.8,0.9)
        if rand1 < London_bound:
            r.append('London')
        else:
            r.append(random.choice(regions))
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
    ncsr_bound = ncsr_bound - csr_bound
    df = pd.DataFrame(df,columns=cols)
    return df,applicants_number,London_bound,csr_bound,ncsr_bound
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
    if day1.ix[1] > 250 and day2.ix[1] > 250:
        dayMetric = True
    else:
        dayMetric = False
    return dayMetric
def regionCalc(df, dict1):
    """Calculates whether the regions are in the ratios below AND if the day metric
    is still correct"""
    regionMetric = 0
    regionDict = dict(Counter(" ".join(df['Region'].values.tolist()).split(" ")).items())
    #print(regionDict)
    validity = 0
    #print(regionDict)
    for region in regionDict:
        regionDict[region] = float(regionDict.get(region))/len(df)
    for key in dict1:
        if (regionDict[key] > dict1[key]-1 and regionDict[key] < dict1[key] + 1):
            validity += 1
    if validity == len(dict1):
        regionMetric = True
    regionMetric = bool(dayCalc(df)*regionMetric)
    return regionMetric
def streamCalc(df,dict1,dict2):
    streamMetric = 0
    streamDict = dict(Counter(" ".join(delegates['Stream'].values.tolist()).split(" ")).items())
    #print(streamDict)
    validity = 0
    for key in dict1:
        #print(dict1[key],streamDict[key])
        if (streamDict[key] > dict1[key] - 5 and streamDict[key] < dict1[key] + 5):
            validity +=1
    if validity == len(dict1):
        streamMetric = True
    streamMetric = bool(regionCalc(df,dict2)*streamMetric)
    return streamMetric
def reindex(df):
    newIndex = range(0,len(df))
    df['Index'] = newIndex
    df = df.set_index('Index')
    return df
def successCalc(df):
    a = dayCalc(df)
    b = regionCalc(df,region_target)
    c = streamCalc(df,stream_target,region_target)
    #print("Day correct: %s \nRegion correct: %s \nStream correct: %s \n" % (c,a,b))
    return a,b,c
data = createData()
test1 = data[0]
for j in range(10000):
    print(data[1],data[2],data[3],data[4])
    status = []
    attempt_no = 0
    test1.to_csv('results/test_data_%d.csv' % attempt_no)
    start_time = time.time()
    success = False
    while success == False:
        if attempt_no > max_attempts:
            break
        iteration = 0
        attempt = "%d.%d" % (j,attempt_no)
        print("Attempt no: %s" % attempt)
        #print(iteration)
        start_iteration_time = time.time()
        applicants = test1
        rows = random.sample(applicants.index, tickets_available)
        delegates = applicants.ix[rows]
        applicants = applicants.drop(rows)
        success_outputs = successCalc(delegates)
        success = success_outputs[2]
        if success == True:
            break
        regionMetric = False
        dayMetric = False
        streamMetric = False
        while streamMetric == False:
            if iteration > max_iterations:
                break
            #print("Starting stream loop %d" % stream_loop)
            while regionMetric == False:
                if iteration > max_iterations:
                    break
                #print("Starting region loop %d" % region_loop)
                while dayMetric == False:
                    #print("Starting day loop %d" % day_loop)
                    success_outputs = successCalc(delegates)
                    dayMetric = success_outputs[0]
                    regionMetric = success_outputs[1]
                    streamMetric = success_outputs[2]
                    success = streamMetric
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
                    iteration += 1
                regionMetric = regionCalc(delegates,region_target)
                if regionMetric == True:
                    break
                dataframes = swapFunc(delegates,applicants)
                delegates = dataframes[0]
                applicants = dataframes[1]
                success_outputs = successCalc(delegates)
                success_outputs = successCalc(delegates)
                success = success_outputs[2]
                regionMetric = success_outputs[1]
                iteration += 1
            streamMetric = success_outputs[2]
            #print(streamMetric)
            if streamMetric == True:
                break
            #print(streamMetric)
            dataframes = swapFunc(delegates,applicants)
            delegates = dataframes[0]
            applicants = dataframes[1]
            success_outputs = successCalc(delegates)
            success = success_outputs[2]
            streamMetric = success
            iteration += 1
        #success = streamMetric
        if streamMetric == True:
            status = [attempt, 'Successful']
            success = True
            metrics.loc[attempt] = [attempt,dayMetric,regionMetric,streamMetric]
            #print("Success! Delegate list compiled")
            day_1 = pd.DataFrame(columns = delegates.columns)
            day_2 = day_1
            reserves_df = day_1
            for index,row in delegates.iterrows():
                if row['Day 1'] == 1 and len(day_1.index) < 250:
                    day_1 = day_1.append(delegates.ix[index])
                elif row['Day 2'] == 1 and len(day_2.index) < 250:
                    day_2.append(delegates.ix[index])
                else:
                    reserves_df.append(delegates.ix[index])
            #print(day_1)
            day_1.to_csv('results/day1_test%s.csv' % attempt)
            day_2.to_csv('results/day2_test%s.csv' % attempt)
            reserves_df.to_csv('results/reserves_test%s.csv' % attempt)
        else:
            success = False
            metrics.loc[attempt] = [attempt,dayMetric,regionMetric,streamMetric]
            attempt_no += 1
            #print("No solutions found in 10,000 iterations. Reshuffling data")
        end_time = (time.time()-start_time)
        times[j] = end_time
    if attempt_no > max_attempts:
        status = [attempt,'Failed after 100 attempts']
        success = False
        metrics.loc[attempt] = [attempt,dayMetric,regionMetric,streamMetric]
        #print("No solutions found in 100 attempts. Testing new data")
    end_time = (time.time()-start_time)
    times[j] = end_time
    status.append(times[j])
    #print("New data")
    with open('results/status.txt', 'a') as f:
        f.write('%s: %s. \nTime: %s\nApplicants: %s\nLondon ratio: %s\nCSR ratio: %s\nNon-CSR: %s\n\n'
        % (status[0],status[1],status[2],data[1],data[2],data[3],data[4]))
    data = createData()
    test1 = data[0]
print("Test complete")
times = pd.DataFrame(times.items(),columns = ['Attempt','Time (s)'])
times.to_csv('results/times.csv')

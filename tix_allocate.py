import pandas as pd
import numpy as np
from collections import Counter
import random
import time
import sys


regions = ['SE','SW','NW','NE','Scotland','Anglia','Wales','Yorkshire','Midlands']
region_target = {'London':.751,"SE":0.037,'SW':0.026,'Wales':0.039,
'Anglia':0.004,'Midlands':0.005,'Yorkshire':0.048,'NW':0.023,'NE':0.017,
'Scotland':0.041}
stream_target = {'CSR':0.7,'non-CSR':0.2,'FT':0.1}
streams = ['CSR','non-CSR','FT']
cols = ['ID','Region','Stream','Day 1','Day 2']
variance = 0.05 #this means a variance of 5%
measures = ['Region','Stream','Day']
times = {}
max_iterations = 9999
max_attempts = 9
tickets_available = 500
def dayCalc(df):
    """This calculates whether there are 250 attendees per day"""
    day1 = df['Day 1'].value_counts()
    day2 = df['Day 2'].value_counts()
    if day1.ix[1] >= 250 and day2.ix[1] >= 250:
        dayMetric = True
    else:
        dayMetric = False
    #print(dayMetric)
    return dayMetric
def createData(j):
    """this function creates rows of random data according to the constraints
    set out below. They can be editted for harder testing"""
    df = []
    this_test_numbers = []
    applicants_number = 600 + (j*100)
    London_bound = random.uniform(0.65,0.85)
    csr_bound = random.uniform(0.6,0.8)
    ncsr_bound = random.uniform(0.1,0.2)
    FT_ratio = 1.0 - (csr_bound + ncsr_bound)
    for i in range(applicants_number):
        r = [i]
        rand1 = random.random()
        rand2 = random.random()
        rand3 = random.randrange(1,4)
        if rand1 < London_bound:
            r.append('London')
        else:
            r.append(random.choice(regions))
        if rand2 < csr_bound:
            r.append(streams[0])
        elif rand2 < (csr_bound + ncsr_bound):
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
    print("London ratio: %f\nCSR ratio: %f\nnCSr ratio: %f\nFT ratio: %f" %
    (London_bound,csr_bound,ncsr_bound,FT_ratio))
    return df,applicants_number,London_bound,csr_bound,ncsr_bound
def calcFunction(label,df,dict1,a,v):
    """Calculates whether selected metric is okay"""
    metric = 0
    calc_dict = dict(Counter(" ".join(df[label].values.tolist()).split(" ")).items())
    validity = 0
    for key in calc_dict:
        calc_dict[key] = float(calc_dict.get(key))/len(df)
    for key in dict1:
        if (calc_dict[key] > (dict1[key] - v) and calc_dict[key] < (dict1[key] + v)):
            validity += 1
    #print("%d/%d" % (validity,len(dict1)))
    if validity == len(dict1):
        metric = True
    if bool(metric * a) == True:
        metric = True
    else:
        metric = False
    return metric
def successCalc(df):
    #print(dayMetric)
    #global dayMetric
    dayMetric = dayCalc(df)
    regionMetric = calcFunction('Region',df,region_target,dayMetric,variance)
    streamMetric = calcFunction('Stream',df,stream_target,regionMetric,variance)
    return dayMetric,regionMetric,streamMetric
def loopFunction(df1,df2,iteration):
    dataframes = swapFunc(df1,df2)
    delegates = dataframes[0]
    applicants = dataframes[1]
    iteration += 1
    return delegates,applicants,iteration
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
def reindex(df):
    newIndex = range(0,len(df))
    df['Index'] = newIndex
    df = df.set_index('Index')
    return df
def __main__():
    for i in range(20):
        success = False
        data = createData(0)
        applicants = data[0]
        applicants_number = data[1]
        rows = random.sample(applicants.index, tickets_available)
        delegates = applicants.ix[rows]
        applicants = applicants.drop(rows)
        outputs = loopFunction(delegates,applicants,0)
        iteration = 0
        i_time = time.time()
        for j in range(10):
            status = []
            attempt_no = 0
            start_time = time.time()
            regionMetric = False
            dayMetric = False
            streamMetric = False
            while success == False:
                attempt = "%d.%d.%d" % (i,j,attempt_no)
                if attempt_no > max_attempts:
                    break
                iteration = 0
                print("Attempt no: %s\nApplicants: %d" % (attempt, applicants_number))
                #print(iteration)
                start_iteration_time = time.time()
                if iteration > max_iterations:
                    break
                success_outcomes = []
                while streamMetric == False:
                    if iteration > max_iterations:
                        break
                    while regionMetric == False:
                        if iteration > max_iterations:
                            break
                        while dayMetric == False:
                            if iteration > max_iterations:
                                break
                            success_outcomes = successCalc(delegates)
                            dayMetric = success_outcomes[0]
                            regionMetric = success_outcomes[1]
                            streamMetric = success_outcomes[2]
                            #print(dayMetric)
                            if dayMetric == True:
                                break
                            else:
                                day_output = loopFunction(delegates,applicants,iteration)
                                delegates = day_output[0]
                                applicants = day_output[1]
                                iteration = day_output[2]
                                success_outcomes = successCalc(delegates)
                                dayMetric = success_outcomes[0]
                                regionMetric = success_outcomes[1]
                                streamMetric = success_outcomes[2]
                                #print("End day loop")
                        if regionMetric == True:
                            break
                        else:
                            region_output = loopFunction(delegates,applicants,iteration)
                            delegates = region_output[0]
                            applicants = region_output[1]
                            iteration = region_output[2]
                            success_outcomes = successCalc(delegates)
                            dayMetric = success_outcomes[0]
                            regionMetric = success_outcomes[1]
                            streamMetric = success_outcomes[2]
                            #print('End region loop')
                    if streamMetric == True:
                        success = True
                        break
                    else:
                        stream_output = loopFunction(delegates,applicants,iteration)
                        delegates = stream_output[0]
                        applicants = stream_output[1]
                        iteration = stream_output[2]
                        success_outcomes = successCalc(delegates)
                        dayMetric = success_outcomes[0]
                        regionMetric = success_outcomes[1]
                        streamMetric = success_outcomes[2]
                        #print("End stream loop")
                if success == True:
                    print("Success!")
                    end_time = time.time() - start_time
                    times[j] = end_time
                    status = [attempt, 'Successful', end_time,iteration]
                    success = True
                    print("Success! Delegate list compiled. Iterating data for current applicant count.")
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
                else:
                    print("Fail!")
                    end_time = time.time() - start_time
                    times[j] = end_time
                    status = [attempt,'Failed after 10,000 operations',end_time,iteration]
                    success = False
                    attempt_no += 1
                    print("No solutions found in 10,000 iterations. Reshuffling data")
                with open('results/status.txt', 'a') as f:
                    f.write('%s: %s. \nTime (s): %s\nIterations required: %d\nApplicants: %s\nLondon ratio: %s\nCSR ratio: %s\nNon-CSR: %s\n\n'
                    % (status[0],status[1],status[2],status[3],data[1],data[2],data[3],data[4]))
                    start_time = time.time()
            attempt = "%d.%d.%d" % (i,j,attempt_no)
            if attempt_no > max_attempts:
                fail_time = time.time() - start_time
                status = [attempt,'Failed after 10 attempts',fail_time]
                success = False
                print("No solutions found in 100 attempts. Testing new data")
            #print("New data")
            data = createData(i)
            test1 = data[0]
        print("Test of %d applicants complete, moving to %d" % (applicants_number, (applicants_number + 100)))
    print("All tests complete")

__main__()

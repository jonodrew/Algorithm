import pandas as pd
import numpy as np
from collections import Counter
import random

"""
read csv
read ratios
analysis: what proportions do we have?
Random select?
Random select according to ratios

OR

Select according to day
apply ratios to results
risks small number in one and unsuitable ratios
hence: ratio global or daily?
Global ratio allows for all OOL on one day

x total df2
y OOL, z London
a CSR, b non-CSR
    a   b
y   +   +
z   +   +

Reduce to stream in ratio 35:10:5 for sum of 800
random selection of region in appropriate ratios
then sort according to preferred day and count

Throw 800 people in at random
Switch out two
If better: keep
If worse: switch back
repeat for 10^x turns
metrics:
stream ratio (overall)
while CSR = 70% and non-CSR = 20% and FT = 10%:
    switch people in and out and as long as above stay within tolerances:
        when in scope, move on to day such that:
            preferred day = +2 and optimise for that day's score
    region ratio (by day? Overall?)
got preferred day? (overall)
"""

"""
create list of dictionaries. Dict. key is delegate code (for anonymity) and
values are stream, region, day
calculate stream metrics
if stream_valid = True:
    calculate region metrics
    if region_valid = True:
        for 1000 turns:
            calcuate day metrics
            swap delegate with low day score
            if region_valid
            calculate day metrics
            if day metrics better:
                keep df1
            if day metrics the same:
                flip a coin
            else:
                swap back

    else:
        swap a delegate from over-subscribed region
        calculate stream metrics
        if stream_valid = False:
            break
        else:
            calculate region metrics


def calculate(columnName, dict.):
    for key in dict:
        count instances of key/len(columnName) for % instances in frame

def streamCalc(CSR_metric, NCSR_metric, FT_metric):
    if CSR_metric > 0.68 and CSR_metric < 0.72:
        CSR_valid = True

    if NCSR_metric > 0.18 and NCSR_metric < 0.22:
        NCSR_valid = True

    if FT_metric > 0.08 and FT_metric < 0.12:
        FT_valid = True

    if CSR_metric + NCSR_metric + FT_metric = 1.0:
        return stream_valid = True


df1 = file.open(heresmyfile.csv)

def __main__(arg):
    generate empty dataframe: index applicant number, columns: stream, region, day
    randomly assign 800 df1 to it
    streamLoop = 0
    regionLoop = 0
    dayLoop = 0
    while iterations <= 1000:
        count up number of stream and calculate %
        if within tolerances:
            while within tolerances:
                regionLoop += 1
                count up according to region and calculate %
                if within tolerances:
                    while within tolerances:
                        dayLoop += 1
                        count up score for days where 2 = perfect, 1 = preferred, 0 = impossible
                        if score = len(list)*2:
                            break and go to the pub
                        else:
                            swap delegate in list with list of df2
                else:
                    swap delegate in list with list of df2
        else:
            swap delegate in list with list of df2



while not stream_valid:
    #code goes in here
    pass
"""
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

def dayCalc(df1):
    day1 = df1['Day 1'].value_counts()
    day2 = df1['Day 2'].value_counts()
    if day1.ix[1] > 250 and day2.ix[1] > 250:
        dayMetric = True
    else:
        dayMetric = False
    return dayMetric

def regionCalc(df):
    regionDict = dict(Counter(" ".join(df['Region'].values.tolist()).split(" ")).items())
    for region in regionList:
        regionDict[region] = float(regionDict.get(region))/len(df1)
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

def reindex(df):
    newIndex = range(0,len(df))
    df['Index'] = newIndex
    df = df.set_index('Index')
    return df

regionList = ['OOL', 'London']

applicants = pd.read_csv('test.csv')

rows = random.sample(applicants.index, 800)

delegates = applicants.ix[rows]


applicants = applicants.drop(rows)


#print (regionDict)

streamDict = dict(Counter(" ".join(delegates['CSR'].values.tolist()).split(" ")).items())

#print (streamDict)

def metricCalc(metricDict):
    for x in metricDict:
        metricDict[x] = float(metricDict.get(x))
    return metricDict



loop = 0
dayMetric = False
for i in range(100):
    while dayMetric == False:
        swapFunc(delegates,applicants)
        dayMetric = dayCalc(delegates)
        if dayMetric == True:
            print("Correct number of delegates per day")
            regionMetric = regionCalc(delegates)
            if regionMetric == False:
                while regionMetric == False:
                    if loop > 1000:
                        break
                    dataframes = swapFunc(delegates,applicants)
                    delegates = dataframes[0]
                    applicants = dataframes[1]
                    print('Swapping candidate')
                    regionMetric = regionCalc(delegates)
                    loop +=1
                    print('This is loop %d' % loop)
            else:
                print ("Correct regional ratio overall")

#! /usr/bin/env python
# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt
import numpy as np
from statsmodels.tsa.seasonal import seasonal_decompose
from matplotlib.font_manager import FontProperties
from mpl_toolkits.mplot3d import Axes3D 
import pandas as pd
from libBase import get_relation_dir, get_config_file_path


min_percentage = 0.3

max_percentage = 5

tracking_length = 8



#Compare x with y using min_percentage and max_percentage
def compare(x, y):
    if x >= y:
        if x/y > max_percentage:
            return True
        else:
            return False
    else:
        if x/y < min_percentage:
            return True
        else:
            return False



def main():
    path = get_config_file_path("3_accounts.csv", "data")
    data_tem = pd.read_csv(path,encoding='utf-8')

    x= data_tem[u'3-交易金额']
    y= data_tem[u'记账日期']
    
    x = np.log10(abs(x)+0.001)

    y = pd.to_datetime(y)
    
    #list of lists
    anomalous_dates = []
    anomalous_ys = []
    anomalous_xs = []

    turning_points = []
    turning_ys = []
    turning_xs = []


    L = len(x)

    for i in range(L):
        if i == 0:
            p_average = 0

            #next 10 days
            future = x[i+1:i+tracking_length+1]
            f_average = np.average(future)

        elif i < tracking_length:

            #past 10 days
            past = x[:i]
            p_average = np.average(past)

            #next 10 days
            future = x[i+1:i+tracking_length+1]
            f_average = np.average(future)
        elif i >= L - tracking_length:

            #past 10 days
            past = x[i - tracking_length:i]
            p_average = np.average(past)

            #next 10 days
            future = x[i:]
            f_average = np.average(future)
        elif i == L-1:

            #past 10 days
            past = x[i - tracking_length:i]
            p_average = np.average(past)

            f_average = 0

        else:
            #past 10 days
            past = x[i - tracking_length:i]
            p_average = np.average(past)

            #next 10 days
            future = x[i+1:i + tracking_length + 1]
            f_average = np.average(future)

        if compare(p_average, x[i]) and compare(f_average, x[i]):
            anomalous_dates.append([y[i], p_average/x[i] * 100, f_average/x[i] * 100])
            anomalous_ys.append(y[i])
            anomalous_xs.append(x[i])


        elif compare(p_average, x[i]) and not compare(f_average, x[i]):
            turning_points.append([y[i], p_average/x[i] * 100, f_average/x[i] * 100])
            turning_ys.append(y[i])
            turning_xs.append(x[i])

    '''
    print("These are the anomalous dates we found: ")


    for data in anomalous_dates:
        date = data[0]
        diff_past = data[1]
        diff_future = data[2]
        print("The anomalous date is: {}".format(date))
        print("The average of past {1} days is: {2} percent of today".format(tracking_length, diff_past))
        print("The average of next {1} days is: {2} percent of today".format(tracking_length, diff_future))
        print("\n")
    '''
    print("The total number of anomalous dates is: {}".format(len(anomalous_dates)))

    
    print("These are the possible dates of business changes: ")

    
    for data in turning_points:
        date = data[0]
        diff_past = data[1]
        diff_future = data[2]
        print("The date when business change occurs is: {}".format(date))
        print("The average of past {0} days is: {1} percent of today".format(tracking_length, diff_past))
        print("The average of next {0} days is: {1} percent of today".format(tracking_length, diff_future))
        print("\n")
    
    
    print("The total number of business change dates is: {}".format(len(turning_points)))


    print(turning_ys)
    print(turning_xs)

    plt.plot(y, x)
    plt.scatter(anomalous_ys, anomalous_xs, marker = "o", color = "red", s = 400)
    plt.scatter(turning_ys, turning_xs, marker = "^", color = "green", s = 400)            
    

    plt.show()

    path2 = get_config_file_path("total_data_with_labels.csv", "data")
    #A Pandas DataFrame
    data_complete =pd.read_csv(path2, encoding = 'utf-8')
    data_complete[u'记账日期']=pd.to_datetime(data_complete[u'记账日期'])

    for date in anomalous_ys:
        anomalous_trans = data_complete.loc[lambda df: df[u'记账日期'] == date]
        anomalous_trans = anomalous_trans.sort(u"交易金额", ascending = False)

    for date in turning_ys:
        turning_trans = data_complete.loc[lambda df: df[u'记账日期'] == date]



if __name__ == "__main__":
    main()






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
    path = get_config_file_path("E29B_account.csv", "data")
    data_tem = pd.read_csv(path,encoding='utf-8')
    path = get_config_file_path("E29B_account_average.csv", "data")
    data_ave = pd.read_csv(path, encoding = 'uft-8')

    x= data_tem[u'交易金额']
    y= data_tem[u'记账日期']

    x2 = data_ave[u'平均金额']
    y2 = data_ave[u'记账日期']
   
 
    x = np.log10(abs(x)+0.001)

    y = pd.to_datetime(y)
    y2 = pd.to_datetime(y2)
    
    #list of lists
    anomalous_dates = []
    anomalous_past_averages = []
    anomalous_future_averages = []


    anomalous_ys = []
    anomalous_xs = []


    turning_points = []
    turning_ys = []
    turning_xs = []


    L = len(x)

    for i in range(L):
        if i == 0:
            p_average = 0
	        p_average2 = 0


            #next 10 days
            future = x[i+1:i+tracking_length+1]
            f_average = np.average(future)

	        future2 = x2[i+1: i + tracking_length + 1]
	        f_average2 = np.average(future2)


        elif i < tracking_length:

            #past 10 days
            past = x[:i]
            p_average = np.average(past)

            past2 = x2[:i]
            p_average2 = np.average(past2)

            #next 10 days
            future = x[i+1:i+tracking_length+1]
            f_average = np.average(future)

            #next 10 days
            future2 = x2[i+1:i+tracking_length+1]
            f_average2 = np.average(future2)

        elif i >= L - tracking_length:

            #past 10 days
            past = x[i - tracking_length:i]
            p_average = np.average(past)

            past2 = x2[i - tracking_length:i]
            p_average2 = np.average(past2)

            #next 10 days
            future = x[i:]
            f_average = np.average(future)

            future2 = x2[i:]
            f_average2 = np.average(future2)


        elif i == L-1:

            #past 10 days
            past = x[i - tracking_length:i]
            p_average = np.average(past)

            past2 = x2[i - tracking_length:i]
            p_average2 = np.average(past2)

            f_average = 0

            f_average2 = 0

        else:
            #past 10 days
            past = x[i - tracking_length:i]
            p_average = np.average(past)

            past2 = x2[i - tracking_length:i]
            p_average2 = np.average(past2)

            #next 10 days
            future = x[i+1:i + tracking_length + 1]
            f_average = np.average(future)

            #next 10 days
            future2 = x2[i+1:i + tracking_length + 1]
            f_average2 = np.average(future2)            
            


        if compare(p_average, x[i]) and compare(f_average, x[i]):
            anomalous_dates.append([y[i], p_average/x[i] * 100, f_average/x[i] * 100])
            anomalous_ys.append(y[i])
            anomalous_xs.append(x[i])
            anomalous_past_averages.append(p_average2)
            anomalous_future_averages.append(f_average2)


        elif compare(p_average, x[i]) and not compare(f_average, x[i]):
            turning_points.append([y[i], p_average/x[i] * 100, f_average/x[i] * 100])
            turning_ys.append(y[i])
            turning_xs.append(x[i])

    
    print("These are the anomalous dates we found: ")


    for data in anomalous_dates:
        date = data[0]
        diff_past = data[1]
        diff_future = data[2]
        print("The anomalous date is: {}".format(date))
        print("The average of past {0} days is: {1} percent of today".format(tracking_length, diff_past))
        print("The average of next {0} days is: {1} percent of today".format(tracking_length, diff_future))
        print("\n")
    
    print("The total number of anomalous dates is: {}".format(len(anomalous_dates)))

    '''
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
    '''

    '''
    plt.plot(y, x)
    plt.scatter(anomalous_ys, anomalous_xs, marker = "o", color = "red", s = 400)
    plt.scatter(turning_ys, turning_xs, marker = "^", color = "green", s = 400)            
    '''

    plt.show()

    path2 = get_config_file_path("total_data_with_labels.csv", "data")
    #A Pandas DataFrame
    data_complete =pd.read_csv(path2, encoding = 'utf-8')
    data_complete[u'记账日期']=pd.to_datetime(data_complete[u'记账日期'])
    data_complete = data_complete.loc[lambda df: df[u'银行账户编号'] == 'FA4A94F378190B6C893E5F45095BE29B'] 

    for date, p_average, f_average in anomalous_ys, anomalous_past_averages, anomalous_future_averages:
	   print("The date when anomalous transactions occur is: ")
	   print(date)
        anomalous_trans = data_complete.loc[lambda df: df[u'记账日期'] == date]

        #anomalous_trans = anomalous_trans.sort_values(by = u"交易金额", ascending = False)
        anomalous_trans["diff"] = anomalous_trans[u"交易金额"].map(lambda a: abs(a - p_average) + abs(a - f_average))
	    anomalous_trans = anomalous_trans.sort_values(by = "diff", ascending = False)

    length = anomalous_trans.shape[0]
	
    if length > 5:
	    anomalous_trans = anomalous_trans.take([i for i in range(5)])
	    anomalous_trans = anomalous_trans.loc[:, [u'事件编号',u'银行账户编号',u'交易套号',u'记账日期', u'交易金额']]
        print(anomalous_trans.to_string())

    '''
    for date in anomalous_ys:
        anomalous_trans = data_complete.loc[lambda df: df[u'记账日期'] == date]
        anomalous_trans = anomalous_trans.sort_values(by = u"交易金额", ascending = False)

    for date in turning_ys:
        turning_trans = data_complete.loc[lambda df: df[u'记账日期'] == date]
    '''
    '''
    accountA = "0748E52AB705B4B3D12F057BDEFD898E"
    accountB = "FA4A94F378190B6C893E5F45095BE29B"
    accountC = "0DDA75B3AAED571183C62DC7CA00EC48"

    A = data_complete[data_complete[u'银行账户编号'] == accountA]
    B = data_complete[data_complete[u'银行账户编号'] == accountB]
    C = data_complete[data_complete[u'银行账户编号'] == accountC]

    datagbA = A.groupby(u'记账日期')
    datagbB = B.groupby(u'记账日期')
    datagbC = C.groupby(u'记账日期')

    to_plot_balances = []

    for date in y:
        #print(date)
        amountA = 0
        amountB = 0
        amountC = 0
        if date in A[u'记账日期']:
            dA = datagbA.get_group(date).sort_values(by = u'交易记录时间')
            amountA = float(dA.last()[u'联机余额'])
        if date in B[u'记账日期']:
            dB = datagbB.get_group(date).sort_values(by = u'交易记录时间')
            amountB = float(dB.last()[u'联机余额'])
        if date in C[u'记账日期']:
            dC = datagbC.get_group(date).sort_values(by = u'交易记录时间')
            amountC = float(dc.last()[u'联机余额'])


        to_plot_balances.append(amountA + amountB + amountC)
        #print(to_plot_balances)
    '''

if __name__ == "__main__":
    main()






#! /usr/bin/env python
# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt
import numpy as np
from statsmodels.tsa.seasonal import seasonal_decompose
from matplotlib.font_manager import FontProperties
from mpl_toolkits.mplot3d import Axes3D 
import pandas as pd

def main():
    #dir_of_inputdata='3_accounts.csv'
    dir_of_inputdata='another_3_accounts.csv'
    data_tem = pd.read_csv(dir_of_inputdata,encoding='utf-8')
    #data_tem = pd.read_csv(dir_of_inputdata,encoding='gbk')
    #data_tem = pd.read_csv(dir_of_inputdata)
    #x= data_tem[u'登入次数']
    #y= data_tem[u'登出次数']
    #z= data_tem[u'登入登出总数目']
    #x= data_tem[u'报错码种类数']
    #y= data_tem[u'报错码总数']
    #z= data_tem[u'登录设备号种类数']
    #x= data_tem['登录时间间隔']
    #y= data_tem['平均登录时间间隔']
    #z= data_tem['总登录次数']
    x= data_tem[u'3-交易金额']
    y= data_tem[u'记账日期']
    x = np.log10(abs(x)+0.001) 
    y = pd.to_datetime(y)
    plt.plot(y,x)
    #ax = plt.subplot(111, projection='3d')
    #ax.scatter(x, y, z)
    #ax = plt.subplot(111)
    #ax.scatter(y,x)
    #decomposition = seasonal_decompose(x, freq=100, two_sided=False)
    #decomposition.plot()
    #plt.subplot(111)
    #plt.plot(x)
    
    #ax.set_xlabel('Transaction Amount')  
    #ax.set_ylabel('Online Balance')
    #ax.set_zlabel('Login')
    #ax.set_zlabel('Number of error codes')  
    #ax.set_ylabel('Total number of errors')
    #ax.set_xlabel('Number of login device number')
    '''ax.set_xlabel('Login time interval')  
    ax.set_ylabel('Average login time interval')
    ax.set_zlabel('Number of login')'''
    plt.show()
if __name__ == "__main__":
    main()






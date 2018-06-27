#!/usr/bin/python
# -*- coding: utf-8 -*-
import pandas as pd

def trade():
    dataset_1 = pd.read_csv('./total_data.csv')
    #dataset_2 = pd.read_csv('./account_with_if_nxh_total.csv')
    #pp=dataset_2[(dataset_2['ct']==1)&(dataset_2['cnt']==2)]
    #trades = set(pp['tradeNum'])
    #trades = ['C01268RC29AA4WJ','C03589R824AAMWJ','C09499R803AAABJ','C00083R823AAMCJ','C05953R915AAAHJ','C04796R214AAAVJ',
    #          'C05396RA10AAVKJ','C01606RB21AA1IJ','C05319RC29AAI9J','C06991R815AAGQJ','C07553RC29ABBRJ','C07553RC29ABC2J',
    #          'C03012R816AAAJJ']
    pp=pd.read_csv('./trade_money.csv',encoding='gbk')
    a = set(pp[u'事件编号'])
    trades =[]
    for i in a:
        trades.append(i.strip())
    datagb = dataset_1.groupby('事件编号')
    tem = pd.DataFrame()
    for tra in trades:
        data_trade = datagb.get_group(tra)
        tem=pd.concat([data_trade,tem])
    tem.to_csv('trade_3.csv',index=False)

def group_by():
    dataset_1 = pd.read_csv('./total_data.csv')
    dataset_1['记账日期']=pd.to_datetime(dataset_1['记账日期'])
    datagb = dataset_1.groupby('记账日期')
    acc_time = set(dataset_1['记账日期'])
    data_tem2 = []
    for acc in acc_time:
        tem = []
        data_acc = datagb.get_group(acc)
        #sum1 = sum(data_acc['交易金额'][data_acc['银行账户编号']=='0748E52AB705B4B3D12F057BDEFD898E'])
        #sum2 = sum(data_acc['交易金额'][data_acc['银行账户编号']=='FA4A94F378190B6C893E5F45095BE29B'])
        #sum3 = sum(data_acc['交易金额'][data_acc['银行账户编号']=='0DDA75B3AAED571183C62DC7CA00EC48'])
        sum1 = sum(data_acc['交易金额'][data_acc['银行账户编号']=='0F60F2F4DE351C11610397AC81581DAE'])
        sum2 = sum(data_acc['交易金额'][data_acc['银行账户编号']=='71E85DC151D764232162F5621868A778'])
        sum3 = sum(data_acc['交易金额'][data_acc['银行账户编号']=='C73F99356848CA08C3979F7DD218211F'])
        sum_total = sum1 + sum2 + sum3
        tem.append(sum_total)
        tem.append(acc)
        data_tem2.append(tem)

    names = ['3-交易金额','记账日期']
    dataset = pd.DataFrame(data_tem2,columns=names)
    p=dataset.sort_values(by="记账日期")
    p.to_csv('./another_3_accounts.csv',index=False,encoding='utf-8')

def main():
    group_by()

if __name__ == "__main__":
    main() 





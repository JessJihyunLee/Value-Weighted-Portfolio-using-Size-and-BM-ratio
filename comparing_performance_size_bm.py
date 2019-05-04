import pandas as pd
from pandas import DataFrame, Series
import numpy as np
import copy
import warnings
from matplotlib import pyplot as plt
import statsmodels.api as sm
warnings.filterwarnings('ignore')

b2m=pd.read_csv("BM.csv")
crsp=pd.read_csv("CRSP_data_HW4.csv")
ff=pd.read_csv("FF.csv")

# Copied data to prevent changing original data
d1=copy.deepcopy(b2m)
d2=copy.deepcopy(crsp)
d3=copy.deepcopy(ff)

d1.head()

pd.concat([d2.head(),d2.tail()])

d3.head()

"""## Preprocessing Data before Analysis"""

# Change into timestamp
d1.public_date=pd.to_datetime(d1.public_date)
d2.date=pd.to_datetime(d2.date)
d3.Month=pd.to_datetime(d3.Month, format='%Y%m')

## Exclude stocks without return data which we cannot invest in
no_stocks=d2[(d2.RET=='B')|(d2.RET=='C')].PERMNO.drop_duplicates()
d4=d2[d2.PERMNO.isin(no_stocks)==False]
### C represent the first day when stocks start to trade again, set it to zero for further data processing, this won't change results 
# Change prices with negative value to positive. Checked that price should be positive based on RET column
d4.PRC=d4.PRC.abs() 
d4.RET=pd.to_numeric(d4.RET)

"""## 1. Smallest 10% market capitalization"""

# Function that takes smallest 10% market cap
def get_tickers1(df):
    number=int(round(len(df.PERMNO.drop_duplicates())*0.1))
    df['mc']=df.PRC_t*df.SHROUT_t
    smallest_mc=df.mc.sort_values(ascending=True)[:number]
    tickers=df.PERMNO.loc[smallest_mc.index]
    return tickers

def get_value_weighted_return(df,tickers):
    temp2=df[df.PERMNO.isin(tickers)]
    temp2['mc']=temp2.PRC_t*temp2.SHROUT_t
    weights=temp2.mc/sum(temp2.mc)
    weighted_return=(weights*temp2.RET_n).sum()
    return weighted_return

def get_monthly_return1(date_index):
    this_month=d4[d4.date==dates.loc[date_index]]
    next_month=d4[d4.date==dates.loc[date_index+1]]
    temp=pd.merge(next_month, this_month, how='inner', left_on='PERMNO', right_on='PERMNO', suffixes=('_n','_t'))
    tickers=get_tickers1(temp)
    return get_value_weighted_return(temp,tickers)

dates=Series(d4.date.unique())
small_mon=Series(dates.index[:-1]).map(get_monthly_return1)
small=np.cumprod(small_mon.add(1))

"""## 2. Top 35% B/M ratio"""

def get_tickers2(df):
    number=int(round(len(df.permno.drop_duplicates())*0.35))
    bm=df.bm.sort_values(ascending=False)[:number]
    tickers=df.permno.loc[bm.index]
    return tickers

def get_monthly_return2(date_index):
    this_month=d4[d4.date==dates.loc[date_index]]
    next_month=d4[d4.date==dates.loc[date_index+1]]
    bm=d1[d1.public_date==dates.loc[date_index]]
    temp=pd.merge(next_month, this_month, how='inner', left_on='PERMNO', right_on='PERMNO', suffixes=('_n','_t'))
    tickers=get_tickers2(bm)
    return get_value_weighted_return(temp,tickers)

High_mon=Series(dates.index[:-1]).map(get_monthly_return2)
High=np.cumprod(High_mon.add(1))

"""## 3. (1)Half-largest and top 35% B/M and (2)Half-smallest and top 35% B/M"""

def get_tickers3(df1, df2):
    number=int(round(len(df1.PERMNO.drop_duplicates())*0.5))
    df1['mc']=df1.PRC_t*df1.SHROUT_t
    largest=df1.mc.sort_values(ascending=False)[:number]
    smallest=df1.mc.sort_values(ascending=False)[number:]
    large_tickers=df1.PERMNO.loc[largest.index]
    tickers1=get_tickers2(df2[df2.permno.isin(large_tickers)])
    small_tickers=df1.PERMNO.loc[smallest.index]
    tickers2=get_tickers2(df2[df2.permno.isin(small_tickers)])
    return [large_tickers, tickers1, small_tickers, tickers2]

def get_monthly_return3(date_index, large=True):
    this_month=d4[d4.date==dates.loc[date_index]]
    next_month=d4[d4.date==dates.loc[date_index+1]]
    bm=d1[d1.public_date==dates.loc[date_index]]
    temp=pd.merge(next_month, this_month, how='inner', left_on='PERMNO', right_on='PERMNO', suffixes=('_n','_t'))
    values=get_tickers3(temp,bm)
    if large==True:
        large=temp[temp.PERMNO.isin(values[0])]
        monthly_return=get_value_weighted_return(large,values[1])
    else:
        small=temp[temp.PERMNO.isin(values[2])]
        monthly_return=get_value_weighted_return(small,values[3])
    return monthly_return

Large_high_mon=Series(dates.index[:-1]).map(lambda x : get_monthly_return3(x,large=True))
Large_high=np.cumprod(Large_high_mon.add(1))
Small_high_mon=Series(dates.index[:-1]).map(lambda x : get_monthly_return3(x,large=False))
Small_high=np.cumprod(Small_high_mon.add(1))

"""## 4. Value Weighted Benchmark"""

def get_monthly_return(date_index):
    this_month=d4[d4.date==dates.loc[date_index]]
    next_month=d4[d4.date==dates.loc[date_index+1]]
    temp=pd.merge(next_month, this_month, how='inner', left_on='PERMNO', right_on='PERMNO', suffixes=('_n','_t'))
    tickers=list(d4.PERMNO.drop_duplicates())
    return get_value_weighted_return(temp,tickers)

#Value weighted all stocks
vw_benchmark=Series(dates.index[:-1]).map(get_monthly_return)
vw_benchmark_cum=np.cumprod(vw_benchmark.add(1))

#Using 'Value Weighted Return Including Dividend' pulled from crsp 
vw_retd=d4[['date','vwretd']].drop_duplicates().vwretd[1:]
vw_retd_cum=np.cumprod(vw_retd.add(1))

returns = DataFrame({'small':small_mon.values, 'high':High_mon.values, 'large_high':Large_high_mon.values, 'small_high':Small_high_mon.values}, index=dates[1:])
cum_returns = DataFrame({'small':small.values, 'high':High.values, 'large_high':Large_high.values, 'small_high':Small_high.values}, index=dates[1:])
cum_returns.head()

"""## Cumulative Return Plot of All Strategies"""

plt.figure(figsize=(20,5))
plt.plot(cum_returns)
plt.legend(list(cum_returns.columns),loc='upper left')
plt.show()

"""## 5. Sharpe Ratio"""

risk_free=Series(d3.RF[1:].values,index=dates[1:])/100
summary = pd.DataFrame()
summary['excess_ret_total']=returns.sub(risk_free,axis=0).add(1).resample('A').agg('prod').sub(1).mean()
summary['vol_total']=returns.apply(np.std)*12**0.5
summary['Sharpe_total']=summary.excess_ret_total/summary.vol_total
summary
##sharpe ratio before 2009
summary_1 = pd.DataFrame()
summary_1['excess_ret_before']=returns.sub(risk_free,axis=0).add(1).resample('A').agg('prod').sub(1)[:'2009-01-01'].mean()
summary_1['vol_before']=returns[:'2009-01-01'].apply(np.std)*12**0.5
summary_1['Sharpe_before']=summary_1.excess_ret_before/summary_1.vol_before
summary_1
##sharpe ratio after 2009
summary_2 = pd.DataFrame()
summary_2['excess_ret_after']=returns.sub(risk_free,axis=0).add(1).resample('A').agg('prod').sub(1)['2009-01-01':].mean()
summary_2['vol_after']=returns['2009-01-01':].apply(np.std)*12**0.5
summary_2['Sharpe_after']=summary_2.excess_ret_after/summary_2.vol_after
summary_2


"""## 6. F-F"""

y=returns.sub(risk_free,axis=0)

def FF_model(S, alpha_only = False):
    X = DataFrame(d3[["Mkt-RF","SMB","HML"]].iloc[1:].values*0.01, columns=["Mkt-RF","SMB","HML"], index=returns.index)
    Y = S
    X2 = sm.add_constant(X)
    est = sm.OLS(Y, X2)
    est2 = est.fit()
    if alpha_only:
        return est2.params[0]
    else  :
        return est2.summary()

"""### Alphas"""

y.apply(lambda x : FF_model(x,alpha_only=True))

"""### Summary of FF for strategy 1"""

FF_model(y.small)

"""### Summary of FF for startegy 2"""

FF_model(y.high)

"""### Summary of FF for startegy 3"""

FF_model(y.large_high)

"""### Summary of FF for startegy 4"""

FF_model(y.small_high)
# -*- coding: utf-8 -*-
"""Untitled0.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1dl_0fBuHe3u0UdqTfmEmYzv7GX1Tq30m
"""

def test_stationarity(timeseries):
  import matplotlib.pyplot as plt
  rolmean = timeseries.rolling(window=5).mean()
  rolstd = timeseries.rolling(window=5).std()

  orig = plt.plot(timeseries, label = 'Original')
  mean = plt.plot(rolmean, label='Rolling mean')
  std = plt.plot(rolstd, label='Rolling std')

  plt.legend(loc='best')
  plt.title('Timeseries data with rolling mean and std. deviation')
  plt.show()


  from statsmodels.tsa.stattools import adfuller

  dftest = adfuller(timeseries)
  dfoutput = pd.Series(dftest[0:4], index = ['Test Statistics', 'Mackinnons approx p-value', 'used lags','NOBS'])
  print(dfoutput)

url = 'https://raw.githubusercontent.com/SimonMcLain/TUS-Engineering-Team-Project/main/Data/HSE/COVID-19_HPSC_County_Statistics_Historic_Data.csv'

import pandas as pd

covid_19_dataset = pd.read_csv(url)

covid_19_dataset.head()

covid_19_dataset.info()

covid_19_dataset['TimeStamp'] = pd.to_datetime(covid_19_dataset['TimeStamp'], infer_datetime_format=True)

indexed_covid_19_dataset = covid_19_dataset.set_index(['TimeStamp'])

indexed_covid_19_dataset.head()

covid_19_confirmed_case_dataset = indexed_covid_19_dataset['ConfirmedCovidCases']

covid_19_confirmed_agg_dataset = covid_19_confirmed_case_dataset.groupby('TimeStamp').sum()

test_stationarity(covid_19_confirmed_agg_dataset)

import numpy as np

covid_19_confirmed_agg_dataset_log_scaled = np.log(covid_19_confirmed_agg_dataset)
 
covid_19_confirmed_agg_dataset_log_scaled = covid_19_confirmed_agg_dataset_log_scaled[covid_19_confirmed_agg_dataset_log_scaled > 0]

test_stationarity(covid_19_confirmed_agg_dataset_log_scaled)

ma = covid_19_confirmed_agg_dataset_log_scaled.rolling(window=6).mean()

covid_19_confirmed_agg_dataset_log_scaled_minus_ma = covid_19_confirmed_agg_dataset_log_scaled - ma

covid_19_confirmed_agg_dataset_log_scaled_minus_ma.dropna(inplace = True)

test_stationarity(covid_19_confirmed_agg_dataset_log_scaled_minus_ma)

covid_19_confirmed_agg_dataset_log_scaled_ps = covid_19_confirmed_agg_dataset_log_scaled.diff(2)

covid_19_confirmed_agg_dataset_log_scaled_ps.dropna(inplace = True)

test_stationarity(covid_19_confirmed_agg_dataset_log_scaled_ps)

from statsmodels.tsa.stattools import acf
from statsmodels.tsa.stattools import pacf

from statsmodels.graphics.tsaplots import plot_acf
from statsmodels.graphics.tsaplots import plot_pacf

import matplotlib.pyplot as plt

lag_acf = acf(covid_19_confirmed_agg_dataset_log_scaled_ps, nlags = 32)
lag_pacf = pacf(covid_19_confirmed_agg_dataset_log_scaled_ps, nlags = 16)

fig,ax = plt.subplots(1,2,figsize=(20,5))

plot_acf(lag_acf, ax = ax[0])
plot_pacf(lag_pacf, lags = 7, ax = ax[1])

plt.show()



def predict(timeseries,p,d,q):

  from statsmodels.tsa.arima_model import ARIMA

  from sklearn.model_selection import train_test_split

  timeseries.dropna(inplace = True)

  train, test = train_test_split(timeseries, test_size = 0.20, shuffle = False)

# ARIMA model
  model_arima = ARIMA(train, order=(p,d,q))

  model_arima_fit = model_arima.fit()

  predictions = model_arima_fit.predict(start='2021-06-22', end = '2021-12-22')

  # from sklearn.metrics import mean_squared_error

  # error = mean_squared_error(test, predictions)

  # print('Test MSE %.5f' % error)

  predict = np.exp(predictions)
  test_set = np.exp(test)

  plt.plot(test_set)
  plt.plot(predict, color='red')
  plt.show()

  from pandas import DataFrame

  residual = DataFrame(model_arima_fit.resid)

  residual.plot(kind='kde')

predict(covid_19_confirmed_agg_dataset_log_scaled_ps, 2,2,10)

from sklearn.model_selection import train_test_split

covid_19_confirmed_agg_dataset_log_scaled_ps.dropna(inplace = True)

train, test= train_test_split(covid_19_confirmed_agg_dataset_log_scaled_ps,test_size = 0.20, shuffle = False)
test.head()
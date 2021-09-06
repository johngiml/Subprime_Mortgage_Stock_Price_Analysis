# By employing visualization (Seaborn: distplots and pairplots, Matplotlib, cufflinks: interactive clustermap, candle plots, simple moving averages, bollinger plot) and pandas skills, this data project is designed to explore substantial changes in the stock prices of major banks during subprime mortgage crisis.
# Initially, I wrote all the lines of code in Jupyter. Then, I converted all the lines of code into a regular Python file.


#Step 1) Importing all the libraries.
from pandas_datareader import data, wb
import pandas as pd
import numpy as np
import datetime
import seaborn as sns
import matplotlib.pyplot as plt
get_ipython().run_line_magic('matplotlib', 'inline')


#Step 2) Obtaining the data and creating a dataframe


# We need to get data using pandas datareader. We will get stock information for the following banks:
# *  Bank of America
# * CitiGroup
# * Goldman Sachs
# * JPMorgan Chase
# * Morgan Stanley
# * Wells Fargo


# **We acquire the stock data from Jan 1st 2006 to Jan 1st 2016 for each of these banks. Set each bank to be a separate dataframe, with the variable name for that bank being its ticker symbol. This will involve a few steps:**
# 1. Set datetime for start and end datetime objects.
# 2. Set the ticker symbol for each bank.
# 3. Use datareader to grab info on the stock.
   

#Set start and end times first. One decade of time.
start = datetime.date(2006,1,1)
end = datetime.date(2021,1,1)


#We grab all the bank data from Yahoo Finance. df below is the same data from Google which is more accurate than the one 
#from Yahoo. Unfortunately, DataReader does not support Google Finance anymore. The file called "all_banks" in the repository
#contains the data from our start date to end date. It would be read by read_pickle.
BAC = data.DataReader("BAC",'yahoo', start, end)
C = data.DataReader("C","yahoo", start, end)
GS = data.DataReader("GS","yahoo",start,end)
JPM = data.DataReader("JPM","yahoo",start,end)
MS = data.DataReader("MS","yahoo",start,end)
WFC = data.DataReader("WFC","yahoo",start,end)
df = pd.read_pickle('all_banks')


#Creating a list of the ticker symbols (as strings) in alphabetical order.
tickers = ["BAC","C","GS","JPM","MS","WFC"]


#Concatenating (combining) all the bank dataframes together
bank_stocks = pd.concat([BAC,C,GS,JPM,MS,WFC], keys=tickers,axis=1)


#Set the column name levels 
bank_stocks.columns.names = ['Bank Ticker','Stock Info'] 


#Just in case that you want to check our dataframe: 
#bank_stocks.head()


#As a test, we can explore the data a bit. For instance, the max Close price for each bank's stock throughout the time period can be found by the following:
round(bank_stocks.xs(key=('Close'), axis=1,level = 'Stock Info').max(),2)  
#By changing Close with any other column name, we can explore any other data.


#Let us create a new empty DataFrame called returns. This dataframe will contain the returns for each bank's stock. Returns are typically defined by the following. 
#return = (ending stock price (p_t) - initial stock price (p_t-1))/initial stock price (p_t-1)
returns = pd.DataFrame()  #for the data imported from Yahoo Finance
returns2 = pd.DataFrame() #for the data imported from Google Finance


# pandas pct_change() method on the Close column creates a column representing this return value. Then, we can create a for loop that goes and for each Bank Stock Ticker creates this returns column and sets it as a column in the returns DataFrame.
for i in tickers: #percentage change for the data extracted from Yahoo
    returns[i + " Return"] = bank_stocks[i].pct_change()['Close']
#check if returns is updated well.
returns
returns.head(5)


for i in tickers: #percentage change for the data extracted from Google
    returns2[i + " Return"] = df[i].pct_change()['Close']
#check if returns2 is updated well
returns2
returns2.head(5)


#Step 3) Visualization and data analysis part


#Let us create a pairplot using seaborn of the returns dataframe. What stock stands out to you? Can you figure out why?
sns.pairplot(returns2) #You can replace return2 with the return column from the data extracted from Yahoo
#However, return column from Yahoo is not accurate for Citigroup
plt.tight_layout()
#Based on the graph, CitiGroup was affected most negatively among the other banks.


# ** Using this returns DataFrame, let us figure out on what dates each bank stock had the best and worst single day returns. 
returns2.idxmin() #minimum return value
returns2.idxmax() #maximum return value


# Let us take a look at the standard deviation of the returns, which stock would you classify as the riskiest over the entire time period? Which would you classify as the riskiest for the year 2015 (as an example)?
returns2.std() #By looking at the standard deviation, CitiGroup seems to be the riskiest.
returns2.loc['2015-01-01':'2015-12-31'].std() #In 2015, the riskiest was MS(Morgan Stanley). We can change the time period to see the full information about a particular year. 


#Let us explore 2015 Morgan Stanley stock price further by creating a distplot using seaborn.
sns.distplot(a=returns2['MS Return'].loc['2015-01-01':'2015-12-31'],bins=100,color = 'green')
plt.grid() #Adding gridlines to the plot.

#Let us explore 2008 CitiGroup stock price further by creating a distplot using seaborn.
sns.distplot(a=returns2['C Return'].loc['2008-01-01':'2008-12-31'], color='red',bins=100)
plt.grid()


#More Visualization
#Importing visualizating libraries including Matplotlib and Seaborn
import matplotlib.pyplot as plt
import seaborn as sns
sns.set_style('whitegrid')
get_ipython().run_line_magic('matplotlib', 'inline') 

#Optional Plotly method imports
import plotly
import cufflinks as cf
cf.go_offline()


#Let us create a line plot showing Close price for each bank for the entire index of time. Three ways below work the same. 
#1)By using multi-index dataframe and df plot method(you can change the size of this plot)
for ticker in tickers:
    bank_stocks[ticker]['Close'].plot(figsize=(12,5))
plt.legend(tickers)

#2) By using Seaborn lineplot with xs method.
sns.lineplot(data=bank_stocks.xs(key=('Close'), axis=1,level = 'Stock Info'))
plt.xlabel('Date')
plt.ylabel('')
plt.legend(tickers)


#3) By using iplot with xs method. (You can trace individual points on the plot.)
bank_stocks.xs(key='Close', axis=1, level='Stock Info').iplot()



#Moving Averages Analysis 
#Let us analyze the moving averages for these stocks in the year 2008. 
#Plotting the rolling 30 day average against the Close Price for Bank Of America's stock for the year 2008.
#Calculating and analyzing moving averages for year 2008. You can simply replace BAC with any other ticker to see the rolling 30 days average of each bank.
plt.figure(figsize = (12,5))
bank_stocks['BAC']['Close'].loc['2008-01-01':'2008-12-31'].rolling(window=30).mean().plot(label = '30 Day Avg')
bank_stocks['BAC']['Close'].loc['2008-01-01':'2008-12-31'].plot(label='BAC CLOSE', color = 'green')
plt.legend()


#By using a heatmap of the correlation between the stocks close price, we can see if the banks affect each other. 
sns.heatmap(data=df.xs(key='Close', axis=1,level = 'Stock Info').corr(),cmap='coolwarm',annot= True) #using Google's data

#Using seaborn's clustermap to cluster the correlations together:
sns.clustermap(data=df.xs(key='Close', axis=1,level = 'Stock Info').corr(),cmap='coolwarm',annot= True)

#We can also use Cufflinks to create an interactive heatmap.
close_corr = bank_stocks.xs(key='Close',axis=1,level='Stock Info').corr()
close_corr.iplot(kind='heatmap',colorscale='rdylbu') 


#Using cufflinks library to create technical analysis plots. 
#1) Creating a candle plot of Bank of America's stock from Jan 1st 2015 to Jan 1st 2016. (Pay attention to the syntax)
BAC[['Open','Low','High','Close']].loc['01-01-2015':'01-01-2016'].iplot(kind='candle')


#2) Creating a Simple Moving Averages plot of Morgan Stanley for the year 2015 by using ta_plot.
MS['Close'].loc['01-01-2015':'12-31-2015'].ta_plot(study='sma',periods=30)


#3) Creating a Bollinger Band Plot for Bank of America for the year 2015 by using ta_plot.
BAC['Close'].loc['2015-01-01':'2015-12-31'].ta_plot(study='boll')

# By employing visualization (Seaborn) and pandas skills, this data project is designed to explore substantial changes in the stock prices of major banks during subprime mortgage crisis.
# Initially, I wrote all the lines of code in Jupyter. Then, I converted all the lines of code into a regular Python file.


#Step 1) Importing All the libraries.
from pandas_datareader import data, wb
import pandas as pd
import numpy as np
import datetime
import seaborn as sns
import matplotlib.pyplot as plt
get_ipython().run_line_magic('matplotlib', 'inline')


#Step 2) Obtaining the Data and creating a dataframe

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


#Step 3) Data Analysis Part


#Let us create a pairplot using seaborn of the returns dataframe. What stock stands out to you? Can you figure out why?
sns.pairplot(returns2) #You can replace return2 with the return column from the data extracted from Yahoo
#However, return column from Yahoo is not accurate for Citigroup
plt.tight_layout()
#Based on the graph, CitiGroup was affected most negatively among the other banks.


# ** Using this returns DataFrame, let us figure out on what dates each bank stock had the best and worst single day returns. 
returns2.idxmin() #minimum return value

returns2.idxmax() #maximum return value





# ** Take a look at the standard deviation of the returns, which stock would you classify as the riskiest over the entire time period? Which would you classify as the riskiest for the year 2015?**

# In[103]:


returns2.std() #By looking at the standard deviation, CitiGroup seems to be the riskiest.


# In[81]:





# In[104]:


returns2.loc['2015-01-01':'2015-12-31'].std() #In 2015, the riskiest was MS.


# In[88]:





# ** Create a distplot using seaborn of the 2015 returns for Morgan Stanley **

# In[105]:


sns.distplot(a=returns2['MS Return'].loc['2015-01-01':'2015-12-31'],bins=100,color = 'green')
plt.grid() #to add gridlines to the plot.


# In[94]:





# ** Create a distplot using seaborn of the 2008 returns for CitiGroup **

# In[106]:


sns.distplot(a=returns2['C Return'].loc['2008-01-01':'2008-12-31'], color='red',bins=100)
plt.grid()


# In[98]:





# ____
# # More Visualization
# 
# A lot of this project will focus on visualizations. Feel free to use any of your preferred visualization libraries to try to recreate the described plots below, seaborn, matplotlib, plotly and cufflinks, or just pandas.
# 
# ### Imports

# In[107]:


import matplotlib.pyplot as plt
import seaborn as sns
sns.set_style('whitegrid')
get_ipython().run_line_magic('matplotlib', 'inline')

# Optional Plotly Method Imports
import plotly
import cufflinks as cf
cf.go_offline()


# ** Create a line plot showing Close price for each bank for the entire index of time. (Hint: Try using a for loop, or use [.xs](http://pandas.pydata.org/pandas-docs/stable/generated/pandas.DataFrame.xs.html) to get a cross section of the data.)**

# In[108]:


#Multiple ways to create this plot:

#1)By using multi-index dataframe and df plot method(you can change the size of this plot)
for ticker in tickers:
    bank_stocks[ticker]['Close'].plot(figsize=(12,5))
plt.legend(tickers)


# In[109]:


#2) By using Seaborn lineplot with xs method.
sns.lineplot(data=bank_stocks.xs(key=('Close'), axis=1,level = 'Stock Info'))
plt.xlabel('Date')
plt.ylabel('')
plt.legend(tickers)


# In[113]:


#3) By using iplot with xs method. (You can trace individual points on the plot.)
bank_stocks.xs(key='Close', axis=1, level='Stock Info').iplot()


# In[17]:





# In[18]:





# In[19]:





# ## Moving Averages
# 
# Let's analyze the moving averages for these stocks in the year 2008. 
# 
# ** Plot the rolling 30 day average against the Close Price for Bank Of America's stock for the year 2008**

# In[207]:


#Calculating and analyzing moving averages for year 2008.
plt.figure(figsize = (12,5))
bank_stocks['BAC']['Close'].loc['2008-01-01':'2008-12-31'].rolling(window=30).mean().plot(label = '30 Day Avg')
bank_stocks['BAC']['Close'].loc['2008-01-01':'2008-12-31'].plot(label='BAC CLOSE', color = 'green')
plt.legend()


# In[141]:





# ** Create a heatmap of the correlation between the stocks Close Price.**

# In[184]:


#By using a heatmap of the correlation between the stocks close price, we can see if the banks affect each other. 
sns.heatmap(data=df.xs(key='Close', axis=1,level = 'Stock Info').corr(),cmap='coolwarm',annot= True) #using Google's data


# In[41]:





# ** Optional: Use seaborn's clustermap to cluster the correlations together:**

# In[185]:


sns.clustermap(data=df.xs(key='Close', axis=1,level = 'Stock Info').corr(),cmap='coolwarm',annot= True)


# In[26]:





# In[217]:


#We can also use Cufflinks to create an interactive heatmap.
close_corr = bank_stocks.xs(key='Close',axis=1,level='Stock Info').corr()
close_corr.iplot(kind='heatmap',colorscale='rdylbu')


# # Part 2 (Optional)
# 
# In this second part of the project we will rely on the cufflinks library to create some Technical Analysis plots. This part of the project is experimental due to its heavy reliance on the cuffinks project, so feel free to skip it if any functionality is broken in the future.

# ** Use .iplot(kind='candle) to create a candle plot of Bank of America's stock from Jan 1st 2015 to Jan 1st 2016.**

# In[204]:


BAC[['Open','Low','High','Close']].loc['01-01-2015':'01-01-2016'].iplot(kind='candle')


# In[125]:





# ** Use .ta_plot(study='sma') to create a Simple Moving Averages plot of Morgan Stanley for the year 2015.**

# In[212]:


MS['Close'].loc['01-01-2015':'12-31-2015'].ta_plot(study='sma',periods=30)


# **Use .ta_plot(study='boll') to create a Bollinger Band Plot for Bank of America for the year 2015.**

# In[214]:


BAC['Close'].loc['2015-01-01':'2015-12-31'].ta_plot(study='boll')


# # Great Job!
# 
# Definitely a lot of more specific finance topics here, so don't worry if you didn't understand them all! The only thing you should be concerned with understanding are the basic pandas and visualization oeprations.

import streamlit as st
import streamlit.components.v1 as components
import sqlite3
import pandas as pd

#Index
from numpy.lib.shape_base import column_stack
import yfinance as yf
import matplotlib.pyplot as plt
import matplotlib as mpl
from datetime import datetime
import datetime
import requests
from requests import get
from bs4 import BeautifulSoup

#Profit
from pandas_profiling import ProfileReport
from streamlit_pandas_profiling import st_profile_report

#Portfolio
import numpy as np
import yfinance 
import yfinance as yf 
yf.pdr_override()
plt.style.use('fivethirtyeight')

def main():
    # Register your pages
    pages = {
        # "Home": Home,
        "Index": Index,
        "Portfolio": Portfolio,
        # "Prediction_model": Prediction_model,
        # "Profit": Profit,
        # 'Statement': Statement,
        # "Stock": Stock,
    }

    st.sidebar.title("App with pages")
    page = st.sidebar.selectbox("Select your page", tuple(pages.keys()))
    pages[page]()

def Index(): 
    page_bg_img = '''
    <style>
    body {
    background-image: url("https://img.freepik.com/free-photo/3d-geometric-abstract-cuboid-wallpaper-background_1048-9891.jpg?size=626&ext=jpg&ga=GA1.2.635976572.1603931911");
    background-size: cover;
    }
    </style>
    '''
    st.markdown(page_bg_img, unsafe_allow_html=True)
    symbols = 'https://raw.githubusercontent.com/Moly-malibu/financesApp/main/bxo_lmmS1.csv'
    df = pd.read_csv(symbols)
    st.markdown("<h1 style='text-align: center; color: #002966;'>Stock Price </h1>", unsafe_allow_html=True)
    start = st.date_input("Please enter date begin Analysis: ") 
    tickerSymbol = st.sidebar.selectbox('Stocks Close and Volume price by Company', (df['Symbol']))
    tickerData = yf.Ticker(tickerSymbol)
    tickerDf = tickerData.history(period='id', start=start, end=None)
    def get_symbol(symbol):
        url = "http://d.yimg.com/autoc.finance.yahoo.com/autoc?query={}&region=1&lang=en".format(symbol)
        result = requests.get(url).json()
        for x in result['ResultSet']['Result']:
            if x['symbol'] == symbol:
                return x['name']
    company_name = get_symbol(tickerSymbol.upper())
    st.write("""# Analysis of """, company_name)
    st.write("""
    ## Closing Price

    """)
    st.line_chart(tickerDf.Close)
    st.write(""" 
    ## Volume Price
    """)
    st.line_chart(tickerDf.Volume)
    st.markdown("<h1 style='text-align: center; color: #002966;'>Stock Price Compared</h1>", unsafe_allow_html=True)
    st.write("""
    **Business** and **Techology** are two fills that have changed the world, both occupy the main ratings in finance, being one of the most highly valued in the stock market leading their owners to be billionaires, in this simple application we can analyze the stock movement and prediction of future price of stock used algoriths and Machile Learning.
    Show are the Stock **Closing Price** and ** Volume** of Stocks by year!
    """)
    st.markdown('Help to take algoritmc decision about stocks')
    company = tickerSymbol1 = st.sidebar.multiselect("Select Companies Stock be compared", (df['Symbol']))
    if company:
        st.subheader("""**Compared Status**""")
        button_clicked = st.sidebar.button("GO")
        analysis = yf.download(tickerSymbol1, start=start, end=None)
        st.write('Analysis', analysis)
        analysis['Adj Close'].plot()
        plt.xlabel("Date")
        plt.ylabel("Adjusted")
        plt.title("Company Stock")
        st.set_option('deprecation.showPyplotGlobalUse', False)
        st.pyplot()

#Portfolio
def Portfolio():
    page_bg_img = '''
    <style>
    body {
    background-image: url("https://images.pexels.com/photos/2748756/pexels-photo-2748756.jpeg?auto=compress&cs=tinysrgb&dpr=1&w=1000");
    background-size: cover;
    }
    </style>
    '''
    st.markdown(page_bg_img, unsafe_allow_html=True)
    symbols = 'https://raw.githubusercontent.com/Moly-malibu/financesApp/main/bxo_lmmS1.csv'
    df = pd.read_csv(symbols)
    st.markdown("<h1 style='text-align: center; color: #002966;'>Portfolio</h1>", unsafe_allow_html=True)
    st.write(""" Make your ***own Portfolio*** with only 5 companies and analyze what will be your profit.""")
    company = tickerSymbol1 = st.sidebar.multiselect("Select minimu 5 Companies to creare the Portfolio", (df['Symbol']))
    if company:
        button_clicked = st.sidebar.button("GO")
        stockStarData = st.date_input("Select Date when you started to investing and create your Portfolio:")
        numAssets = len(tickerSymbol1)
        st.write('***you have*** ' +str(numAssets) + ' ***Assets in your Portafolio.***')
        def getmyportfolio(stock=tickerSymbol1, start=stockStarData, end=None):
            data = yf.download(tickerSymbol1, start=start, end=end)['Adj Close']
            return data
        my_stocks = getmyportfolio(tickerSymbol1)
        st.write(my_stocks)
        daily_return = my_stocks.pct_change(1)
        daily_return.corr()
        daily_return.cov()
        daily_return.var()
        daily_return.std()
        st.write('***Stock Return ***',daily_return)
        st.write('***Stock Correlation ***',daily_return.corr())
        st.write('***Stock Covariance Matrix for Return***',daily_return.cov())
        st.write('***Stock Variance ***',daily_return.var())
        st.write('***Stock Volatility ***', daily_return.std())
    #Visualization
        plt.figure(figsize=(12, 4.5))
        for c in daily_return.columns.values:
            plt.plot(daily_return.index, daily_return[c], lw=2, label=c)
        plt.legend(loc='upper right', fontsize=10)
        plt.title('Volatility')
        plt.ylabel('Dayly Return')
        plt.xlabel('Date')
        plt.style.use('dark_background')
        st.set_option('deprecation.showPyplotGlobalUse', False)
        st.pyplot()
    #get Growth Investment
        dailyMeanSimpleReturns = daily_return.mean()
        st.write('***Daily Mean Simple Return:*** ', dailyMeanSimpleReturns)
        randomWeights = np.array([0.4, 0.1, 0.3, 0.1, 0.1])
        portfoliosimpleReturn = np.sum(dailyMeanSimpleReturns*randomWeights)
        st.write('***Daily Expected Portfolio Return:*** '+str(portfoliosimpleReturn))
        st.write('***Expected Annualised Portfolio Return:*** ' + str(portfoliosimpleReturn*253))
        dailyCumulSimpleReturn = (daily_return+1).cumprod()
        st.write('***Growth of Investment:*** ', dailyCumulSimpleReturn)
    #Visualization
        plt.figure(figsize=(12.2, 4.5))
        for c in dailyCumulSimpleReturn.columns.values:
            plt.plot(dailyCumulSimpleReturn.index, dailyCumulSimpleReturn[c], lw=2, label=c)
        plt.legend(loc='upper left', fontsize=10)
        plt.xlabel('Date')
        plt.ylabel('Growth fo $1 Investment')
        plt.title('Daily Cumulative Returns')
        st.set_option('deprecation.showPyplotGlobalUse', False)
        st.pyplot()

if __name__ == "__main__":
   main()

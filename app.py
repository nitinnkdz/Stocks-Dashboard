import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import numpy as np
import tweepy
import config
from fbprophet import Prophet
from fbprophet.plot import plot_plotly
from plotly import graph_objs as go
import requests , redis
import yfinance as yf
import cufflinks as cf
from cryptocmd import CmcScraper
import json
from PIL import Image
from datetime import datetime, timedelta

auth = tweepy.OAuthHandler(config.TWITTER_CONSUMER_KEY, config.TWITTER_CONSUME_SECRET)
auth.set_access_token(config.TWITTER_ACCESS_TOKEN,config.TWITTER_ACCESS_TOKEN_SECRET)
api = tweepy.API(auth)

st.title("STOCK SYSTEM")
st.sidebar.write("DASHBOARD")
Dashboard = st.sidebar.selectbox("Select the dashboard",('Signal','Information','Fundamentals','News','StockTwits','Twitter','Reddit','ML-Forecast Stock Prices','crypto Prediction','Patterns','TradingView' ))
st.header(Dashboard)


if Dashboard == 'Information':
    # Retrieving tickers data
    
    ticker_list = pd.read_csv('https://raw.githubusercontent.com/nitinnkdz/s-and-p-500-companies/master/data/constituents_symbols.txt',error_bad_lines=False)
    tickerSymbol = st.sidebar.selectbox('Stock ticker', ticker_list)
    tickerData = yf.Ticker(tickerSymbol) # 
    tickerDf = tickerData.history(period="max")  

    # Ticker information
    string_logo = '<img src=%s>' % tickerData.info['logo_url']
    st.markdown(string_logo, unsafe_allow_html=True)

    string_name = tickerData.info['longName']
    st.header('**%s**' % string_name)

    string_summary = tickerData.info['longBusinessSummary']
    st.info(string_summary)

    st.header('**Ticker data**')
    st.write(tickerDf)

    # Bollinger bands
    st.header('**Bollinger Bands**')
    qf = cf.QuantFig(tickerDf, title='First Quant Figure', legend='top', name='GS')
    qf.add_bollinger_bands()
    fig = qf.iplot(asFigure=True)
    st.plotly_chart(fig)

if Dashboard == 'News':
    nsymbol = st.sidebar.text_input("Symbol", value= 'TSLA', max_chars=10)
    url= f"https://api.polygon.io/v2/reference/news?limit=100&sort=published_utc&ticker={nsymbol}&published_utc.gte=2021-04-26&apiKey=l7CZdzU2ElYhYaDCj5QQeyVUxMgr7UPZ"
    r = requests.get(url)
    data = r.json()
    for results in data['results']:
        st.header(results['title'])
        st.write(results['author'])
        st.write(results['published_utc'])
        st.image(results['image_url'])
        st.write(results['article_url'])
        
         
if Dashboard == 'Twitter':
  for username in config.TWITTER_USERNAMES:
        user = api.get_user(username)
        tweets = api.user_timeline(username)

        st.subheader(username)
        st.image(user.profile_image_url)
        
        for tweet in tweets:
            if '$' in tweet.text:
                words = tweet.text.split(' ')
                for word in words:
                    if word.startswith('$') and word[1:].isalpha():
                        symbol = word[1:]
                        st.write(symbol)
                        st.write(tweet.text)
                        st.image(f"https://finviz.com/chart.ashx?t={symbol}")

if Dashboard == 'Reddit':
    num_days = st.sidebar.slider('Number of days', 1, 30, 3)
    st.subheader('Data fetched from subreddit\wallstreetbets')
    st.write("Timescaledb is not avalible")

if Dashboard == 'Patterns':
        st.subheader('Run pattern recognition algorithm on a symbol. Support double top/bottom, triple top/bottom, head and shoulders, triangle, wedge, channel, flag, and candlestick patterns.')
        syslist = pd.read_csv('https://raw.githubusercontent.com/nitinnkdz/s-and-p-500-companies/master/data/constituents_symbols.txt',error_bad_lines=False)
        pattern = st.sidebar.selectbox('Symbol', syslist)
        url1= f"https://finnhub.io/api/v1//scan/pattern?symbol={pattern}&resolution=D&token=c2tiabaad3i9opcku8r0"
        pr = requests.get(url1)
        patt= pr.json()
        st.write(patt)

if Dashboard == 'Signal':
    st.markdown("This application allows you to examine Fundamentals, Market News, and Investor Sentiment.This application\
                can provide you with a variety of stock-related information, as well as forecast the future value of any\
                cryptocurrency/stocks! Under the hood, the application is developed with Streamlit (the front-end) and \
                the Facebook Prophet model, which is an advanced open-source forecasting model established by Facebook.\
                You can choose to train for any number of days in the future model on all available data or a specific \
                period range. Finally, the prediction results can be plotted on both a normal and log scale.This \
                application makes use of the Twitter API to deliver tweets connected to a ticker, as well as other APIs\
                such as Iex Cloud, Finnhub, and Polygon.io to provide various information\about a specific symbol. \
                This features trading-view to analyse charts as well.")

    components.html(
        """
        <!-- TradingView Widget BEGIN -->
    <div class="tradingview-widget-container">
      <div class="tradingview-widget-container__widget"></div>
      <div class="tradingview-widget-copyright"><a href="https://in.tradingview.com" rel="noopener" target="_blank"><span class="blue-text">Crypto</span></a> <span class="blue-text">and</span> <a href="https://in.tradingview.com" rel="noopener" target="_blank"><span class="blue-text">ECONOMIC INDICATORS</span></a> by TradingView</div>
      <script type="text/javascript" src="https://s3.tradingview.com/external-embedding/embed-widget-market-quotes.js" async>
      {
      "width": "980",
      "height": "610",
      "symbolsGroups": [
        {
          "name": "Indices",
          "originalName": "Indices",
          "symbols": [
            {
              "name": "FOREXCOM:SPXUSD",
              "displayName": "S&P 500"
            },
            {
              "name": "FOREXCOM:NSXUSD",
              "displayName": "Nasdaq 100"
            },
            {
              "name": "FOREXCOM:DJI",
              "displayName": "Dow 30"
            },
            {
              "name": "INDEX:NKY",
              "displayName": "Nikkei 225"
            },
            {
              "name": "INDEX:DEU30",
              "displayName": "DAX Index"
            },
            {
              "name": "FOREXCOM:UKXGBP",
              "displayName": "UK 100"
            },
            {
              "name": "NSE:NIFTY",
              "displayName": "NIFTY 50"
            },
            {
              "name": "BSE:SENSEX"
            },
            {
              "name": "TVC:HSI"
            },
            {
              "name": "TASE:TASE"
            },
            {
              "name": "SSE:000009"
            },
            {
              "name": "HOSE:VN100"
            }
          ]
        },
        {
          "name": "Commodities",
          "originalName": "Commodities",
          "symbols": [
            {
              "name": "CME_MINI:ES1!",
              "displayName": "S&P 500"
            },
            {
              "name": "CME:6E1!",
              "displayName": "Euro"
            },
            {
              "name": "COMEX:GC1!",
              "displayName": "Gold"
            },
            {
              "name": "NYMEX:CL1!",
              "displayName": "Crude Oil"
            },
            {
              "name": "NYMEX:NG1!",
              "displayName": "Natural Gas"
            },
            {
              "name": "CBOT:ZC1!",
              "displayName": "Corn"
            }
          ]
        },
        {
          "name": "Bonds",
          "originalName": "Bonds",
          "symbols": [
            {
              "name": "CME:GE1!",
              "displayName": "Eurodollar"
            },
            {
              "name": "CBOT:ZB1!",
              "displayName": "T-Bond"
            },
            {
              "name": "CBOT:UB1!",
              "displayName": "Ultra T-Bond"
            },
            {
              "name": "EUREX:FGBL1!",
              "displayName": "Euro Bund"
            },
            {
              "name": "EUREX:FBTP1!",
              "displayName": "Euro BTP"
            },
            {
              "name": "EUREX:FGBM1!",
              "displayName": "Euro BOBL"
            }
          ]
        },
        {
          "name": "Forex",
          "originalName": "Forex",
          "symbols": [
            {
              "name": "FX:EURUSD"
            },
            {
              "name": "FX:GBPUSD"
            },
            {
              "name": "FX:USDJPY"
            },
            {
              "name": "FX:USDCHF"
            },
            {
              "name": "FX:AUDUSD"
            },
            {
              "name": "FX:USDCAD"
            },
            {
              "name": "FX_IDC:INRUSD"
            },
            {
              "name": "FX_IDC:INREUR"
            }
          ]
        },
        {
          "name": "Crypto",
          "symbols": [
            {
              "name": "BINANCE:BTCUSDT"
            },
            {
              "name": "BINANCE:ETHUSDT"
            },
            {
              "name": "BINANCE:DOGEUSDT"
            },
            {
              "name": "BINANCE:ADAUSDT"
            },
            {
              "name": "BINANCE:LTCUSDT"
            },
            {
              "name": "BINANCE:MATICUSDT"
            },
            {
              "name": "BINANCE:XRPUSDT"
            },
            {
              "name": "BINANCE:SHIBUSDT"
            },
            {
              "name": "BINANCE:ALPHAUSDT"
            },
            {
              "name": "BINANCE:PSGUSDT"
            },
            {
              "name": "BINANCE:AXSUSDT"
            }
          ]
        },
        {
          "name": "ECONOMIC INDICATORS",
          "symbols": [
            {
              "name": "FRED:FEDFUNDS"
            },
            {
              "name": "FRED:WM2NS"
            },
            {
              "name": "FRED:UNRATE"
            },
            {
              "name": "ISM:MAN_PMI"
            },
            {
              "name": "FRED:GDP"
            },
            {
              "name": "FRED:INDPRO"
            },
            {
              "name": "FRED:PI"
            },
            {
              "name": "FRED:CP"
            },
            {
              "name": "FRED:PCE"
            },
            {
              "name": "FRED:EMRATIO"
            },
            {
              "name": "FRED:ISRATIO"
            },
            {
              "name": "FRED:FPCPITOTLZGUSA"
            }
          ]
        }
      ],
      "showSymbolLogo": true,
      "colorTheme": "light",
      "isTransparent": false,
      "locale": "in"
    }
      </script>
    </div>
    <!-- TradingView Widget END
 
   """,
        height=1100, width=1100,
    )



if Dashboard == 'StockTwits':
    symboltws = st.sidebar.text_input("Symbol", value='AAPL', max_chars=10)
    r1 = requests.get(f"https://api.stocktwits.com/api/2/streams/symbol/{symboltws}.json")
    data1 = r1.json()
    for message in data1['messages']:
        st.image(message['user']['avatar_url'])
        st.write(message['user']['username'])
        st.write(message['created_at'])
        st.write(message['body'])

if Dashboard == 'Fundamentals':
        t_list1 = pd.read_csv('https://raw.githubusercontent.com/nitinnkdz/s-and-p-500-companies/master/data/constituents_symbols.txt',error_bad_lines=False)
        tSymbol1 = st.sidebar.selectbox('Stock ticker', t_list1)
        url = f"https://cloud.iexapis.com/v1/stock/{tSymbol1}/logo?token=sk_418c4e3699a241b68e83b5fddfa797de"
        ld =requests.get(url)
        response_json = ld.json()
        st.image(response_json['url'])
        r2 = requests.get(f'https://api.polygon.io/v2/reference/financials/{tSymbol1}?limit=1&apiKey=l7CZdzU2ElYhYaDCj5QQeyVUxMgr7UPZ')
        live = r2.json()
        for results in live['results']:
            st.subheader('Assets')
            st.write(results['assets'])
            st.subheader('Book Value Per Share')
            st.write(results['bookValuePerShare'])
            st.subheader('Capital Expenditure')
            st.write(results['capitalExpenditure'])
            st.subheader('Cash and Equivalent in USD')
            st.write(results['cashAndEquivalentsUSD'])
            st.subheader('Cost of Revenue')
            st.write(results['costOfRevenue'])
            st.subheader('Consolidated Income')
            st.write(results['consolidatedIncome'])
            st.subheader('Current Ratio')
            st.write(results['currentRatio'])
            st.subheader('Debt TO Equity Ratio')
            st.write(results['debtToEquityRatio'])
            st.subheader('Debt')
            st.write(results['debt'])
            st.subheader('Deferred Revenue')
            st.write(results['deferredRevenue'])
            st.subheader('Depreciation Amortization And Accretion')
            st.write(results['depreciationAmortizationAndAccretion'])
            st.subheader('Deposits')
            st.write(results['deposits'])
            st.subheader('Dividend Yeild')
            st.write(results['dividendYield'])
            st.subheader('Dividend per basic common share')
            st.write(results['dividendsPerBasicCommonShare'])
            st.subheader('EBITDA Margin')
            st.write(results['EBITDAMargin'])
            st.subheader('Earnings Before Interest Taxes Depreciation Amortization USD')
            st.write(results['earningsBeforeInterestTaxesDepreciationAmortizationUSD'])
            st.subheader('Earnings Per Basic Share')
            st.write(results['earningsPerBasicShare'])
            st.subheader('Earnings Per Diluted Share')
            st.write(results['earningsPerDilutedShare'])
            st.subheader('Shareholder Equity')
            st.write(results['shareholdersEquityUSD'])
            st.subheader('Enterprise value')
            st.write(results['enterpriseValue'])
            st.subheader('Enterprise value over EBITDA')
            st.write(results['enterpriseValueOverEBITDA'])
            st.subheader('Free CashFlow Per Share')
            st.write(results['freeCashFlowPerShare'])
            st.subheader('Gross Profit')
            st.write(results['grossProfit'])
            st.subheader('Gross Margin')
            st.write(results['grossMargin'])
            st.subheader('Invested Capital')
            st.write(results['investedCapital'])
            st.subheader('Inventory')
            st.write(results['inventory'])
            st.subheader('Investment')
            st.write(results['investments'])
            st.subheader('Totaal Libalities')
            st.write(results['totalLiabilities'])
            st.subheader('Market Capitalization')
            st.write(results['marketCapitalization'])
            st.subheader('Net Cash Flow')
            st.write(results['netCashFlow'])
            st.subheader('Net Income')
            st.write(results['netIncome'])
            st.subheader('Profit Margin')
            st.write(results['profitMargin'])
            st.subheader('Operrating Expenses')
            st.write(results['operatingExpenses'])
            st.subheader('Opertaing Income')
            st.write(results['operatingIncome'])
            st.subheader('Payout Ratio')
            st.write(results['payoutRatio'])
            st.subheader('Price to Book Value')
            st.write(results['priceToBookValue'])
            st.subheader('Price Earnings')
            st.write(results['priceEarnings'])
            st.subheader('Price to Earnings Ratio')
            st.write(results['priceToEarningsRatio'])
            st.subheader('Price Sales')
            st.write(results['priceSales'])
            st.subheader('Price to Sales Ratio')
            st.write(results['priceToSalesRatio'])
            st.subheader('Revenues')
            st.write(results['revenues'])
            st.subheader('Research And Development Expense')
            st.write(results['researchAndDevelopmentExpense'])
            st.subheader('Share Factor')
            st.write(results['shareFactor'])
            st.subheader('Shares')
            st.write(results['shares'])
            st.subheader('Weighted Average Shares')
            st.write(results['weightedAverageShares'])
            st.subheader('Sales Per Shares')
            st.write(results['salesPerShare'])
            st.subheader('Tax-Assets')
            st.write(results['taxAssets'])
            st.subheader('Tax-Libalities')
            st.write(results['taxLiabilities'])
            st.subheader('Income Tax Expense')
            st.write(results['incomeTaxExpense'])
            st.subheader('Working Capital')
            st.write(results['workingCapital'])


if Dashboard == 'TradingView':
    components.html(
        """
        <!-- TradingView Widget BEGIN -->
    <div class="tradingview-widget-container">
    <div id="tradingview_6e5da"></div>
    <div class="tradingview-widget-copyright"><a href="https://in.tradingview.com/symbols/NASDAQ-AAPL/" rel="noopener" target="_blank"><span class="blue-text">AAPL Chart</span></a> by TradingView</div>
    <script type="text/javascript" src="https://s3.tradingview.com/tv.js"></script>
    <script type="text/javascript">
     new TradingView.widget(
    {
    "width": 980,
    "height": 610,
    "symbol": "NASDAQ:AAPL",
    "timezone": "Etc/UTC",
    "theme": "dark",
    "style": "1",
    "locale": "in",
    "toolbar_bg": "#f1f3f6",
    "enable_publishing": false,
    "withdateranges": true,
     "range": "ALL",
     "hide_side_toolbar": false,
    "allow_symbol_change": true,
    "calendar": true,
     "studies": [
    "BollingerBandsR@tv-basicstudies",
    "RSI@tv-basicstudies",
    ],
    "container_id": "tradingview_6e5da"
     }
     );
    </script>
    </div>
    <!-- TradingView Widget END -->
   """,
   height=1100,width = 1100,                 
)
   

if Dashboard == 'ML-Forecast Stock Prices':
    START = st.date_input('Start Date',datetime.date(2011,1,1))
    END = st.date_input('End date')
    stockslist = pd.read_csv('https://raw.githubusercontent.com/nitinnkdz/s-and-p-500-companies/master/data/constituents_symbols.txt',error_bad_lines=False)
    selected_stock = st.selectbox('Select the stock for prediction', stockslist)

    n_years = st.slider('Years of prediction:', 1, 5)
    period = n_years * 365


    @st.cache
    def load_data(ticker):
        data = yf.download(ticker, START, END)
        data.reset_index(inplace=True)
        return data

        
    data_load_state = st.text('Loading data...')
    data = load_data(selected_stock)
    data_load_state.text('Loading data... done!')

    st.subheader('Raw data')
    st.write(data.tail())

    def plot_raw_data():
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=data['Date'], y=data['Open'], name="stock_open"))
        fig.add_trace(go.Scatter(x=data['Date'], y=data['Close'], name="stock_close"))
        fig.layout.update(title_text='Time Series data with Rangeslider', xaxis_rangeslider_visible=True)
        st.plotly_chart(fig)
        
    plot_raw_data()

    df_train = data[['Date','Close']]
    df_train = df_train.rename(columns={"Date": "ds", "Close": "y"})

    m = Prophet()
    m.fit(df_train)
    future = m.make_future_dataframe(periods=period)
    forecast = m.predict(future)

    st.subheader('Forecast data')
    st.write(forecast.tail())
        
    st.write(f'Forecast plot for {n_years} years')
    fig1 = plot_plotly(m, forecast)
    st.plotly_chart(fig1)

    st.write("Forecast components")
    fig2 = m.plot_components(forecast)
    st.write(fig2)

if Dashboard == 'crypto Prediction':
    st.markdown(
        """
    <style>
    .big-font {
        fontWeight: bold;
        font-size:22px !important;
    }
    </style>
    """, unsafe_allow_html=True)

    ### Select ticker & number of days to predict on
    selected_ticker = st.sidebar.text_input("Select a cryptocurrency", "BTC")
    period = int(
        st.sidebar.number_input('Number of days to predict:', min_value=0, max_value=1000000, value=365, step=1))
    training_size = int(
        st.sidebar.number_input('Training set (%) size:', min_value=10, max_value=100, value=100, step=5)) / 100


    ### Initialise scraper without time interval
    @st.cache
    def load_data(selected_ticker):
        init_scraper = CmcScraper(selected_ticker)
        df = init_scraper.get_dataframe()
        min_date = pd.to_datetime(min(df['Date']))
        max_date = pd.to_datetime(max(df['Date']))
        return min_date, max_date


    data_load_state = st.sidebar.text('Loading data...')
    min_date, max_date = load_data(selected_ticker)
    data_load_state.text('Loading data... done!')

    ### Select date range
    date_range = st.sidebar.selectbox("Select the timeframe to train the model on:",
                                      options=["All available data", "Specific date range"])

    if date_range == "All available data":

        ### Initialise scraper without time interval
        scraper = CmcScraper(selected_ticker)

    elif date_range == "Specific date range":

        ### Initialise scraper with time interval
        start_date = st.sidebar.date_input('Select start date:', min_value=min_date, max_value=max_date, value=min_date)
        end_date = st.sidebar.date_input('Select end date:', min_value=min_date, max_value=max_date, value=max_date)
        scraper = CmcScraper(selected_ticker, str(start_date.strftime("%d-%m-%Y")), str(end_date.strftime("%d-%m-%Y")))

    ### Pandas dataFrame for the same data
    data = scraper.get_dataframe()

    st.subheader('Raw data')
    st.write(data.head())


    ### Plot functions
    def plot_raw_data():
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=data['Date'], y=data['Close'], name="Close"))
        fig.layout.update(title_text='Time Series data with Rangeslider', xaxis_rangeslider_visible=True)
        st.plotly_chart(fig)


    def plot_raw_data_log():
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=data['Date'], y=data['Close'], name="Close"))
        fig.update_yaxes(type="log")
        fig.layout.update(title_text='Time Series data with Rangeslider', xaxis_rangeslider_visible=True)
        st.plotly_chart(fig)


    ### Plot (log) data
    plot_log = st.checkbox("Plot log scale")
    if plot_log:
        plot_raw_data_log()
    else:
        plot_raw_data()

    ### Predict forecast with Prophet
    if st.button("Predict"):

        df_train = data[['Date', 'Close']]
        df_train = df_train.rename(columns={"Date": "ds", "Close": "y"})

        ### Create Prophet model
        m = Prophet(
            changepoint_range=training_size,  # 0.8
            yearly_seasonality='auto',
            weekly_seasonality='auto',
            daily_seasonality=False,
            seasonality_mode='multiplicative',  # multiplicative/additive
            changepoint_prior_scale=0.05
        )

        ### Add (additive) regressor
        for col in df_train.columns:
            if col not in ["ds", "y"]:
                m.add_regressor(col, mode="additive")

        m.fit(df_train)

        ### Predict using the model
        future = m.make_future_dataframe(periods=period)
        forecast = m.predict(future)

        ### Show and plot forecast
        st.subheader('Forecast data')
        st.write(forecast.head())

        st.subheader(f'Forecast plot for {period} days')
        fig1 = plot_plotly(m, forecast)
        if plot_log:
            fig1.update_yaxes(type="log")
        st.plotly_chart(fig1)

        st.subheader("Forecast components")
        fig2 = m.plot_components(forecast)
        st.write(fig2)

st.sidebar.write("Created By Nitin Kohli")
st.sidebar.write("[LinkedIn](https://www.linkedin.com/in/nitin-kohli/)")




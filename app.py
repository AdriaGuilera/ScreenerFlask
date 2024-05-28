from flask import Flask, render_template, request
import yfinance as yf
import talib as ta
from values import marketcap as MC
from values import ma as MA
import pandas as pd
import os

app = Flask(__name__)

@app.route("/")
def index():
    marketCap = request.args.get("market-cap", None)
    ma = request.args.get("MovingAvarage", None)
    stocks = {}
    sectors = []
    with open("datasets/nasdaq.csv") as f:
        df = pd.read_csv(f)
        sectors = pd.unique(df["Industry"])
    if marketCap and ma:
        num_mc = MC[marketCap]
        print(num_mc)
        num_ma = MA[ma]
        print(num_ma)
        with open("datasets/nasdaq.csv") as f:
            df = pd.read_csv(f)
            Stocksdf = df.loc[df['Market Cap'] > num_mc, ["Symbol", "Name"]]
            for _,stock in Stocksdf.iterrows():
                filename = f'datasets/Stocks/{stock["Symbol"]}.csv'
                if os.path.exists(filename):
                    data = pd.read_csv(filename)
                    if(len(data["Close"]) < num_ma):
                        print(stock["Symbol"] + " has not enough data")
                        continue

                    close = float("{:.2f}".format(data["Close"].iloc[-1]))
                    sma = float("{:.2f}".format(ta.SMA(data["Close"], num_ma).iloc[-1]))
                    change = float("{:.2f}".format((close-sma)/sma*100))
                    rsi = round(ta.RSI(data["Close"], 14).iloc[-1])

                    sevenDayChange = float("{:.2f}".format((data["Close"].iloc[-1] - data["Close"].iloc[-2])/data["Close"].iloc[-2]*100))
                    monthlyChange = float("{:.2f}".format((data["Close"].iloc[-1] - data["Close"].iloc[-4])/data["Close"].iloc[-4]*100))

                
                    stocks[stock["Symbol"]] = {
                        'name':  stock["Name"],
                        'close': close,
                        'sma': sma,
                        'smachange': change,
                        'rsi': rsi,
                        'day': sevenDayChange,
                        'month': monthlyChange,
                        # Add other data as needed
                    }

    return render_template('index.html', stocks=stocks, sectors=sectors)
    
@app.route("/snapshot")
def snapshot():
    with open("datasets/nasdaq.csv") as f:
        df = pd.read_csv(f)
        Stocksdf = df[["Symbol"]]
        for _,stock in Stocksdf.iterrows():
            filename = f'datasets/Stocks/{stock["Symbol"]}.csv'
            if not os.path.exists(filename):
                data = yf.download(str(stock["Symbol"]), period=str(50) + 'wk', interval='1wk', progress=False)
                data.to_csv(filename)
    return {
        'code': 'success'
    }

@app.route("/update")
def update():
    try:
        data = yf.download("MSFT", period='3y', interval='1wk', progress=False)
    except Exception as e:
        print(f"Error downloading data: {e}")
    return{
        'code': 'success'
    }
        
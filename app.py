
from flask import Flask, render_template, request, jsonify
import yfinance as yf
import pandas_ta as ta
from values import marketcap as MC
from values import ma as MA
import pandas as pd
import os
import country_converter as coco
from datetime import datetime

app = Flask(__name__)


@app.route("/")
def index():
    marketCap = request.args.get("market-cap", None)
    ma = request.args.get("MovingAvarage", None)
    sec = request.args.get("sector", None)
    stocks = {}
    sectors = [ ]
    closes = { }
    with open("datasets/nasdaq.csv") as f:
        df = pd.read_csv(f)
        sectors = pd.unique(df.loc[pd.notna(df["Sector"]), "Sector"])
    if marketCap and ma and sec:
        num_mc = MC[marketCap]
        num_ma = MA[ma]

        with open("datasets/nasdaq.csv") as f:
            df = pd.read_csv(f)
            Stocksdf = []
            if(sec != "All"):
                Stocksdf = df.loc[(df['Market Cap'] > num_mc) & (df["Sector"] == sec), ["Symbol", "Name"]]
            else:
                Stocksdf = df.loc[(df['Market Cap'] > num_mc), ["Symbol", "Name","Country"]]

            for _,stock in Stocksdf.iterrows():
                filename = f'datasets/Stocks/{stock["Symbol"]}.csv'
                if os.path.exists(filename):
                    data = pd.read_csv(filename)
                    if(len(data["Close"]) < num_ma):
                        print(stock["Symbol"] + " has not enough data")
                        continue
                    closes[stock["Symbol"]] = data["Close"].tolist()
                    close = float("{:.2f}".format(data["Close"].iloc[-1]))
                    sma = float("{:.2f}".format(ta.sma(data["Close"], num_ma).iloc[-1]))
                    change = float("{:.2f}".format((close-sma)/sma*100))
                    rsi = round(ta.rsi(data["Close"], 14).iloc[-1])

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
                        'country': coco.convert(names=stock["Country"], to='ISO2')
                        # Add other data as needed
                    }

    
    return render_template('index.html', stocks=stocks, sectors=sectors,closes=closes)
    
    
@app.route("/snapshot")
def snapshot():
    with open("datasets/nasdaq.csv") as f:
        df = pd.read_csv(f)
        Stocksdf = df[["Symbol"]]
        for _,stock in Stocksdf.iterrows():
            filename = f'datasets/Stocks/{stock["Symbol"]}.csv'
            if not os.path.exists(filename):
                data = yf.download(str(stock["Symbol"]), start="2024-01-01", end=datetime.today(), interval='1wk', progress=False)
                data.to_csv(filename)
    return {
        'code': 'success'
    }

@app.route("/update")
def update():
    with open("datasets/nasdaq.csv") as f:
        df = pd.read_csv(f)
        Stocksdf = df[["Symbol"]]["Symbol"].tolist()
        for stock in Stocksdf:
            try:
                f = open(f'datasets/Stocks/{stock}.csv')
                data = pd.read_csv(f)
                if(len(data["Close"]) < 50):
                    print(stock + " has not enough data")
                    os.remove(f'datasets/Stocks/{stock}.csv')
                    df = df.loc[df['Symbol'] != stock]
                    continue
            except FileNotFoundError:
               df = df.loc[df['Symbol'] != stock]
            else:
                print("Found ")
        df.to_csv("datasets/nasdaq.csv",index=False)
    return{
        'code': 'success'
    }

@app.route("/summary")
def summary():
    sectors = {}
    with open("datasets/nasdaq.csv") as f:
        df = pd.read_csv(f)
        sectorslist= pd.unique(df.loc[pd.notna(df["Sector"]), "Sector"]).tolist()
        for sector in sectorslist:
            maxsector = -120
            maxstock = ""
            average = []
            minsector = 1000
            minstock = ""
            over= 0
            stocks = df.loc[(df["Sector"] == sector) & (df["Market Cap"] > 300000000), "Symbol"].tolist()
            for stock in stocks:
                filename = f'datasets/Stocks/{stock}.csv'
                with open(filename) as ff:
                    data = pd.read_csv(ff)
                    if(len(data["Close"]) < 50):
                        print(stock + " has not enough data")
                        continue
                    sma = float("{:.2f}".format(ta.sma(data["Close"], 50).iloc[-1]))
                    close = float("{:.2f}".format(data["Close"].iloc[-1]))
                    if(close > sma):
                        over += 1

                    monthlyChange = float("{:.2f}".format((data["Close"].iloc[-1] - data["Close"].iloc[-4])/data["Close"].iloc[-4]*100))
                    average.append(monthlyChange)
                    if monthlyChange > maxsector:
                        maxsector = monthlyChange
                        maxstock = stock
                    if monthlyChange < minsector:
                        minsector = monthlyChange
                        minstock = stock
        
            average = sum(average)/len(average)
            over = over/len(stocks)*100
            sectors[sector] = {
                'average': f'{average:.2f}%',
                'min': f'{minsector}%',
                'minstock': minstock,
                'max': f'{maxsector}%',
                'maxstock': maxstock,
                'over50ma': f'{over:.2f}%'
            }

                
    return render_template('summary.html', sectors=sectors)

@app.route("/stock/<symbol>")
def stockinfo(symbol):
    data = yf.Ticker(symbol).info



    
    return render_template('stockinfo.html', stock=symbol, data=data)

if __name__ == "__main__":
    app.run(debug=True)

#hola
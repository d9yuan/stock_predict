import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt
from yahoo_fin import stock_info as si

def predict(stock_name, yang):
    stock = yf.Ticker(stock_name)
    ten_days_data = stock.history(period="10d")
    l = len(ten_days_data)
    real_open = round(si.get_live_price(stock_name), 4)
    real_price = round(si.get_live_price(stock_name), 4)
    for i in range(0, l):
        if ((ten_days_data.iloc[i]["Close"] - ten_days_data.iloc[i]["Open"]) > 0):
            m = "Rise"
        else:
            m = "Fall"
        if (m == "Fall"):
            open_at_fall = ten_days_data.iloc[i]["Open"]
            for k in range(i, l):
                close = ten_days_data.iloc[k]["Close"]
                openp = ten_days_data.iloc[k]["Open"]
                open_at_fall = max(openp, open_at_fall)
                if (k == l - 1):
                    close = real_price
                    openp = real_open
                if ((close - openp) > 0):
                    m1 = "Rise"
                else:
                    m1 = "Fall"
                if (k - i < 3):
                    if (m1 == "Rise"):
                        break

                if (m1 == "Rise"):
                    if ((close - open_at_fall) > 0):
                        if (k == l - 1):
                            yang.append(stock_name)
                            return
                    break
        
def predict_mult(stocks):
    yang = []
    for string in stocks:
        predict(string, yang)
    return yang

def five_year_predict(stock):
    stock_d = yf.Ticker(stock)
    five_year_data = stock_d.history(period="5y") 
    young = []
    l = len(five_year_data)
    for i in range(0, l):
        if ((five_year_data.iloc[i]["Close"] - five_year_data.iloc[i]["Open"]) > 0):
            m = "Rise"
        else:
            m = "Fall"
        if (m == "Fall"):
            open_at_fall = five_year_data.iloc[i]["Open"]
            for k in range(i, l):
                open_today = five_year_data.iloc[k]["Open"]
                open_at_fall = max(open_today, open_at_fall)
                if ((five_year_data.iloc[k]["Close"] - five_year_data.iloc[k]["Open"]) > 0):
                    m1 = "Rise"
                else:
                    m1 = "Fall"
                if (k - i < 2):
                    if (m1 == "Rise"):
                        break

                if (m1 == "Rise"):
                    if ((five_year_data.iloc[k]["Close"] - open_at_fall) > 0):
                        a = [-1]
        
                        for s in range(k + 1, min(k + 8, l)):
                            a.append(five_year_data.iloc[s]["High"])
                        a = max(a)
                        young.append((five_year_data.iloc[k].name.strftime("%Y-%m-%d"), five_year_data.iloc[k]["Close"], a))


                    break
    return young

def mult_five_year_predict(stocks):
    retval = []
    for stock in stocks:
        df = five_year_predict(stock)
        if (len(df) == 0):
            continue
        retval.append((stock, pd.DataFrame(data=df, columns=['date', 'price when fall', 'highest after rise'])))
    return retval
    
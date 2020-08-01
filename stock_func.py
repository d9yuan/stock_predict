import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt
from yahoo_fin import stock_info as si

def predict(stock_name, yang, period_time="10d"):
    stock = yf.Ticker(stock_name)
    ten_days_data = stock.history(period=period_time)
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

def given_period_predict(stock, period_time="10d", lower_day=2, lowest_day = 2, lower_control=True, lowest_control=True, allow_duplicates=False):
    stock_d = yf.Ticker(stock)
    period_time_data = stock_d.history(period=period_time) 
    young = []
    l = len(period_time_data)
    i = -1
    while i < l - 1:
        i += 1
        if ((period_time_data.iloc[i]["Close"] - period_time_data.iloc[i]["Open"]) > 0):
            m = "Rise"
        else:
            m = "Fall"
        if (m == "Fall"):
            open_at_fall = period_time_data.iloc[i]["Open"]
            for k in range(i, l):
                open_today = period_time_data.iloc[k]["Open"]
                open_at_fall = max(open_today, open_at_fall)
                if ((period_time_data.iloc[k]["Close"] - period_time_data.iloc[k]["Open"]) > 0):
                    m1 = "Rise"
                else:
                    m1 = "Fall"
                if (k - i < lower_day):
                    if (m1 == "Rise"):
                        i = k + 1
                        break

                if (m1 == "Rise"):
                    if (lowest_control == True):
                        if (k >= lowest_day):
                            b = []
                            for m in range(1 , lowest_day + 1):
                                b.append(period_time_data.iloc[k - m]["Low"])
                            bmin = min(b)
                            if (open_today >= bmin):
                                continue
                    if (lower_control == False):
                        a = [-1]
                        for s in range(k + 1, min(k + 8, l)):
                            a.append(period_time_data.iloc[s]["High"])
                        a = max(a)
                        young.append((period_time_data.iloc[k].name.strftime("%Y-%m-%d"), period_time_data.iloc[k]["Close"], a))
                    else:
                        if ((period_time_data.iloc[k]["Close"] - open_at_fall) > 0):
                            a = [-1]
                            for s in range(k + 1, min(k + 8, l)):
                                a.append(period_time_data.iloc[s]["High"])
                            a = max(a)
                            young.append((period_time_data.iloc[k].name.strftime("%Y-%m-%d"), period_time_data.iloc[k]["Close"], a))
                    if (not allow_duplicates):
                        i = k + 1
                    break
    return young

def mult_given_period_predict(stocks, period_time="10d", lower_day=2, lowest_day = 2,lower_control=True, lowest_control=True, allow_duplicates=False):
    retval = []
    for stock in stocks:
        df = given_period_predict(stock, period_time, lower_day, lowest_day, lower_control, lowest_control, allow_duplicates)
        if (len(df) == 0):
            continue
        retval.append((stock, pd.DataFrame(data=df, columns=['date', 'price when fall', 'highest after rise'])))
    return retval
    
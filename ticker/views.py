# from asyncio.windows_events import NULL
from django.shortcuts import render
import numpy as np
import pandas as pd
import pandas_datareader as pdr
from pandas_datareader import data as wb
from pandas_datareader._utils import RemoteDataError
from datetime import date, timedelta
# ticker_list=pd.read_csv("tickercode.csv")
# print(ticker_list)
def index(request):
    ticker = request.POST.get('ticker', None)
    # ticker_name = ticker_name
    # ticker_code = ticker
    if ticker:
    # if request.method == "POST":
        # if request.method == "POST":
        # ticker=request.POST.get('ticker', None)
        ticker_name = str(request.POST.get('ticker_name',None))

        # ticker_code = str(request.POST.get('ticker_code',None))
        ticker_code = ticker
        try:
            # Variables
            # start_date='2017-1-1'
            start_date = (date.today()-timedelta(days=360))
            data_source = 'yahoo'
            # Get Data From Internet
            ticker_data = wb.DataReader(ticker, data_source=data_source, start=start_date)
            df = pd.DataFrame(ticker_data)
            ticker_date = ticker_data.index
            # last_ten_days=ticker_date[-10:]
            # last_20_days=ticker_date[-20:]
            # last_20_days_lastDayExcluded=ticker_date[-20:-1]
            last_10_days_lastDayExcluded = ticker_date[-10:-1]
            c = df['Close']
            # o=df['Open']
            h = df['High']
            l = df['Low']
            last_price = c[-1]
            # prices=[o,c,h,l]
            # doji=(o==c)
            # eksi=(c<o)
            # artı=(c>o)
            # Finding Max in Last 10 Days
            def max10(x):
                max10 = max(x[last_10_days_lastDayExcluded])
                print("Hedef Fiyat = {:.2f}".format(max10))
                return max10
            # Finding Min in Last Days

            def min10(x):
                min10 = min(x[last_10_days_lastDayExcluded])
                print("Min10 low = {:.2f}".format(min10))
                return min10
            # max10(h)
            # min10(l)
            maxInDate = max(h[ticker_date])
            minInDate = min(l[ticker_date])
            # maxIn30Days=max(h[ticker_date[-30:-1]])
            # print(maxIn30Days)
            max10 = max(h[last_10_days_lastDayExcluded])
            min10 = min(l[last_10_days_lastDayExcluded])
            # Risk Reward
            potentialReward = max10-last_price
            risk = last_price-min10
            # RecommendationList
            recommendationList = ['Yeni Dip Yapıyor Pozisyona Girme', 'Yeni Zirve Arayışı', 'AL', 'Pozisyona Girme']
            new_low = str(recommendationList[0])
            new_high = str(recommendationList[1])
            buy = str(recommendationList[2])
            dontBuy = str(recommendationList[3])
            def tradeable():
                if (last_price < min10):
                    str_ticker = str("{}".format(ticker))
                    recommendation = new_low
                    str_lastPrice = str("{:.2f} ".format(c[-1]))
                    str_earn_potential = ''
                    str_loss_potential = ''
                    str_target_SalePrice = ''
                    str_stopLoss = ''
                    if(minInDate < last_price):
                        str_lastPrice = str("{:.2f} ".format(c[-1]))
                        str_stopLoss = str("{:.2f}".format(minInDate))
                        return str_ticker, recommendation, str_lastPrice, str_earn_potential, str_loss_potential, str_target_SalePrice, str_stopLoss
                    return str_ticker, recommendation, str_lastPrice, str_earn_potential, str_loss_potential, str_target_SalePrice, str_stopLoss
                elif (last_price > max10):
                    str_ticker = str("{}".format(ticker))
                    recommendation = new_high
                    str_lastPrice = str("{:.2f} ".format(c[-1]))
                    str_earn_potential = ''
                    str_loss_potential = str("{:.2f}".format(last_price-max10))
                    str_target_SalePrice = ''
                    str_stopLoss = str("{:.2f}".format(max10))
                    if(maxInDate > last_price):
                        if((maxInDate-last_price)*2 > (last_price-max10)):
                            recommendation = buy
                        else:
                            recommendation = dontBuy
                        str_earn_potential = str("{:.2f}".format(maxInDate-last_price))
                        str_target_SalePrice = str("{:.2f}".format(maxInDate))
                    return str_ticker, recommendation, str_lastPrice, str_earn_potential, str_loss_potential, str_target_SalePrice, str_stopLoss
                else:
                    if (potentialReward > risk*2):
                        str_ticker = str("{}".format(ticker))
                        recommendation = buy
                        str_stopLoss = str("{:.2f}".format(min10))
                        str_lastPrice = str("{:.2f} ".format(c[-1]))
                        str_earn_potential = str("{:.2f}".format(potentialReward))
                        str_loss_potential = str("{:.2f}".format(risk))
                        str_target_SalePrice = str("{:.2f}".format(max10))
                        return str_ticker, recommendation, str_lastPrice, str_earn_potential, str_loss_potential, str_target_SalePrice, str_stopLoss

                    else:
                        str_ticker = str("{}".format(ticker))
                        recommendation = dontBuy
                        str_stopLoss = str("{:.2f}".format(min10))
                        str_lastPrice = str("{:.2f} ".format(c[-1]))
                        str_earn_potential = str("{:.2f}".format(potentialReward))
                        str_loss_potential = str("{:.2f}".format(risk))
                        str_target_SalePrice = str("{:.2f}".format(max10))
                        str_stopLoss = str("{:.2f}".format(min10))
                        return str_ticker, recommendation, str_lastPrice, str_earn_potential, str_loss_potential, str_target_SalePrice, str_stopLoss
            tradeable()
        except RemoteDataError:
            alert="Hisse Kodunu Yanlış Girdiniz"
            return render(request,'index.html',{'alert':alert})
        except ValueError:
            alert="ValueError"
            return render(request,'index.html',{'alert':alert})
        except KeyError:
            alert="Grafik Bilgisi yok"
            return render(request,'index.html',{'alert':alert})
        except UnboundLocalError:
            alert="Lütfen Aradığınız Hisse Bilginisini Giriniz"
            return render(request,'index.html',{'alert':alert})
            
        context = {
            'ticker': ticker,
            'str_ticker': tradeable()[0],
            'recommendation': tradeable()[1],
            'str_earn_potential': tradeable()[3],
            'str_loss_potential': tradeable()[4],
            'str_lastPrice': tradeable()[2],
            'str_target_SalePrice': tradeable()[5],
            'str_stopLoss': tradeable()[6],
            'ticker_code': ticker_code,
            'ticker_name' : ticker_name,
        }
        return render(request, "index.html", context,{'ticker_code':ticker_code})
    elif ticker and ticker is None :
        return render(request, 'index.html')
    else:
        return render(request, 'index.html')
    return render(request, "index.html")

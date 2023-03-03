import pyupbit
import pandas as pd
import matplotlib.pyplot as plt

access = "your-access"
secret = "your-secret"


# 4시간 봉 가져오기
def get_4h(ticker):
    df = pyupbit.get_ohlcv(ticker, interval="minute240", count=200)
    df.to_csv("4hour.csv")


def get_close():
    df = pd.read_csv("4hour.csv", index_col = 0)
    return df


# 4시간 역추세-볼린저밴드 그리기
def bb1(x, length=5, multi=4):
    df = pd.DataFrame(x)
    df['ma'] = df['close'].rolling(length).mean()
    print(df['close'].rolling(length))
    df['stddev'] = df['close'].rolling(length).std(ddof = 0)
    df['upper'] = df['ma'] + multi * df['stddev']
    df['lower'] = df['ma'] - multi * df['stddev']
    #df = df[length-1:]
    print(df)
    df.to_csv("4hourWBollin.csv")
    print(df.loc[(df.low < df.lower)])
    df.loc[(df.low < df.lower)].to_csv("long.csv")
    print(df.loc[(df.high > df.upper)])
    df.loc[(df.high > df.upper)].to_csv("short.csv")
    print(df.loc['2023-02-12 01:00:00'])
""" 
    plt.figure(figsize=(9, 5))
    plt.plot(df.index, df['close'], label='Close')
    plt.plot(df.index, df['upper'], linestyle='dashed', label='Upper band')
    plt.plot(df.index, df['ma'], linestyle='dashed', label='Moving Average'+str(length))
    plt.plot(df.index, df['lower'], linestyle='dashed', label='Lower band')
    plt.title('Bollinger('+str(length)+' days, '+str(multi) + ' stddevs)')
    plt.legend(loc='best')
    plt.show()
"""


def auto_trade(ticker):
    pass


def get_balance(ticker):
    """잔고 조회"""
    balances = upbit.get_balances()
    for b in balances:
        if b['currency'] == ticker:
            if b['balance'] is not None:
                return float(b['balance'])
            else:
                return 0
    return 0


def get_current_price(ticker):
    """현재가 조회"""
    return pyupbit.get_orderbook(ticker=ticker)["orderbook_units"][0]["ask_price"]


# 로그인
upbit = pyupbit.Upbit(access, secret)
print("autotrade start")


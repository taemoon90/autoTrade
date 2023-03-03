import pyupbit
import pandas as pd
import matplotlib.pyplot as plt

access = "your-access"
secret = "your-secret"


# 4시간 역추세-볼린저밴드 그리기
def bb1(ticker, length=5, multi=4):
    df = pyupbit.get_ohlcv(ticker, interval="minute240", count=5)
    df['ma'] = df['close'].rolling(length).mean()
    print(df['close'].rolling(length))
    df['stddev'] = df['close'].rolling(length).std(ddof = 0)
    df['upper'] = df['ma'] + multi * df['stddev']
    df['lower'] = df['ma'] - multi * df['stddev']
    df = df[length-1:]
    print(df)
    print(df.loc[(df.low < df.lower)])
    print(df.loc[(df.high > df.upper)])

bb1("KRW-BTC")

def auto_trade(ticker):
    pass



def get_current_price(ticker):
    """현재가 조회"""
    return pyupbit.get_orderbook(ticker=ticker)["orderbook_units"][0]["ask_price"]

'''
# 로그인
upbit = pyupbit.Upbit(access, secret)
print("autotrade start")

# 자동매매 시작
while True:
    try:
        if

        else:

    except Exception as e:
        print(e)
        time.sleep(1)
'''
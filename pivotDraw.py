import time
import numpy as np
import pyupbit
import pandas as pd
import datetime
from matplotlib import pyplot as plt


def get_ohlcv(ticker):
    """ohlcv 가져오기"""
    df = pyupbit.get_ohlcv(ticker, interval="day", count=30)
    df.to_csv("btckrw.csv", index=False)


def get_pivot(data):
    """고/저점 구하기 Pivot Point https://junyoru.tistory.com/163"""
    v = pd.read_csv(data).copy()

    past_diff = v['high'].pct_change(1).values # +면 어제보다 오늘 가격이 더 높다는 뜻
    future_diff = v['high'].pct_change(-1).values # +면 오늘보다 내일 가격이 더 낮다는 뜻
    pivot_high_order1 = np.array([1 if past_diff[i] > 0 and past_diff[i] * future_diff[i] > 0 else 0 for i in range(len(past_diff))])

    past_diff = v['low'].pct_change(1).values # +면 어제보다 오늘 가격이 더 높다는 뜻
    future_diff = v['low'].pct_change(-1).values # +면 오늘보다 내일 가격이 더 낮다는 뜻
    pivot_low_order1 = np.array([-1 if past_diff[i] < 0 and past_diff[i] * future_diff[i] > 0 else 0 for i in range(len(past_diff))])

    v['pivot_order1'] = pivot_high_order1 + pivot_low_order1

    # PIVOT ORDER2
    v2 = v[v['pivot_order1'] > 0]

    past_diff = v2['high'].pct_change(1).values # +면 어제보다 오늘 가격이 더 높다는 뜻
    future_diff = v2['high'].pct_change(-1).values # +면 오늘보다 내일 가격이 더 낮다는 뜻
    pivot_high_order2 = np.array([1 if past_diff[i] > 0 and past_diff[i] * future_diff[i] > 0 else 0 for i in range(len(past_diff))])
    pivot_order2 = pd.DataFrame(pivot_high_order2,index=v2.index,columns=['pivot_order2_high'])
    v = v.join(pivot_order2)

    v2 = v[v['pivot_order1'] < 0]
    past_diff = v2['low'].pct_change(1).values # +면 어제보다 오늘 가격이 더 높다는 뜻
    future_diff = v2['low'].pct_change(-1).values # +면 오늘보다 내일 가격이 더 낮다는 뜻
    pivot_low_order2 = np.array([-1 if past_diff[i] < 0 and past_diff[i] * future_diff[i] > 0 else 0 for i in range(len(past_diff))])
    pivot_order2 = pd.DataFrame(pivot_low_order2,index=v2.index,columns=['pivot_order2_low'])
    v = v.join(pivot_order2)
    v.fillna(0,inplace=True)

    v['pivot_order2'] = v['pivot_order2_high'] + v['pivot_order2_low']
    del v['pivot_order2_high']
    del v['pivot_order2_low']

    # PIVOT ORDER3
    v2 = v[v['pivot_order2'] > 0]
    past_diff = v2['high'].pct_change(1).values # +면 어제보다 오늘 가격이 더 높다는 뜻
    future_diff = v2['high'].pct_change(-1).values # +면 오늘보다 내일 가격이 더 낮다는 뜻
    pivot_high_order3 = np.array([1 if past_diff[i] > 0 and past_diff[i] * future_diff[i] > 0 else 0 for i in range(len(past_diff))])
    pivot_order3 = pd.DataFrame(pivot_high_order3,index=v2.index,columns=['pivot_order3_high'])
    v = v.join(pivot_order3)

    v2 = v[v['pivot_order2'] < 0]
    past_diff = v2['low'].pct_change(1).values # +면 어제보다 오늘 가격이 더 높다는 뜻
    future_diff = v2['low'].pct_change(-1).values # +면 오늘보다 내일 가격이 더 낮다는 뜻
    pivot_low_order3 = np.array([-1 if past_diff[i] < 0 and past_diff[i] * future_diff[i] > 0 else 0 for i in range(len(past_diff))])
    pivot_order3 = pd.DataFrame(pivot_low_order3,index=v2.index,columns=['pivot_order3_low'])
    v = v.join(pivot_order3)
    v.fillna(0,inplace=True)

    v['pivot_order3'] = v['pivot_order3_high'] + v['pivot_order3_low']
    del v['pivot_order3_high']
    del v['pivot_order3_low']

    return v


def draw_pivot(data):
    v2 = data.copy()

    plt.plot(v2['low'], linewidth=0.5, c='k')
    plt.plot(v2['high'], linewidth=0.5, c='k')

    plt.scatter(v2[v2['pivot_order1'] > 0].index, v2[v2['pivot_order1'] > 0]['high'], s=10, c='k')
    plt.scatter(v2[v2['pivot_order1'] < 0].index, v2[v2['pivot_order1'] < 0]['low'], s=10, c='k')

    plt.scatter(v2[v2['pivot_order2'] > 0].index, v2[v2['pivot_order2'] > 0]['high'], s=50, c='b')
    plt.scatter(v2[v2['pivot_order2'] < 0].index, v2[v2['pivot_order2'] < 0]['low'], s=50, c='r')

    plt.scatter(v2[v2['pivot_order3'] > 0].index, v2[v2['pivot_order3'] > 0]['high'], s=150, c='b', marker='s')
    plt.scatter(v2[v2['pivot_order3'] < 0].index, v2[v2['pivot_order3'] < 0]['low'], s=150, c='r', marker='s')
    plt.show()
    # print(v.head) // 데이터 확인


# get_ohlcv("KRW-BTC") # 데이터 가져오기
draw_pivot(get_pivot("btckrw.csv")) # btckrw 으로 피봇 그리기

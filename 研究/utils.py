#coding=utf-8

from kuanke.user_space_api import *
import talib
import numpy

# 获取股票N天内(含当天)的移动平均线，即N天内的平均价格
def ma(security, n):
    # 获取股票的收盘价
    closes = attribute_history(security, n-1, '1d', ('close'))['close'].values
    # 增加当日数据去计算
    cur_close = attribute_history(security, 1, '1m', ('close'))['close'].values
    closes = numpy.concatenate((closes,cur_close))
    # log.info(closes)
    # 返回N天内(含当天)的平均价格
    return closes.mean()

# 获取股票是否在多头趋势内
# 5日均线 > 10 日均线 > 20日均线则表示在多头趋势内
def is_bull_market(security):
    return ma(security, 5) > ma(security, 10) and ma(security, 10) > ma(security, 20)

# 是否占上N日生命线
def is_lifeline(self, security, n, data):
    return data[security].close > self.ma(security, n)

# 获取MACD，含当前数据，适用于按分钟回测
def macd(security, fastperiod=12, slowperiod=26, signalperiod=9) :
    closes = attribute_history(security, slowperiod*5, '1d', ('close'))['close'].values
    # 增加当日数据去计算
    cur_close = attribute_history(security, 1, '1m', ('close'))['close'].values
    closes = numpy.concatenate((closes,cur_close))
    #log.info('prices:', close)
    macdDIFF, macdDEA, macd = talib.MACDEXT(closes, fastperiod=fastperiod, fastmatype=1, slowperiod=slowperiod, slowmatype=1, signalperiod=signalperiod, signalmatype=1)
    macd = macd * 2
    #log.info("%s macd ==> DIFF=%s, DEA=%s, macd=%s", security, macdDIFF[-1], macdDEA[-1], macd[-1])
    return macdDIFF, macdDEA, macd

# 获取股票的位置,默认为前610交易日
def stock_position(security, days=610):
    # 获取股票的520日价格
    close_data = attribute_history(security, days, '1d', ['low','high'])
    min = close_data['low'].min()
    max = close_data['high'].max()
    current_price = attribute_history(security, 20, '1m', ['close'])['close'][-1]
    # 从610日最低价到当前价的涨幅
    recent_gains = (current_price-min)/min*100
    # 从610日最高价到当前价的跌幅
    recent_decline = (max-current_price)/max*100
    log.info("==> %s股票的位置：最低价=%s，最高价=%s，当前价=%s，近期涨幅=%.2f，近期跌幅=%.2f",security,min,max,current_price, recent_gains, recent_decline)
    return recent_gains, recent_decline
    # 如果涨幅大于2倍则过滤
    #if(recent_gains > 2)
    #    return True

# TODO: 根据量价关系评分排序，上涨放量下跌缩量，红量多于阴量

# TODO: MACD 5\15\30\60分钟及日线底背离

# TODO: MACD 5\15\30\60分钟及日线顶背离

# TODO: 根据当前K线的位置评分，如：当前股票在近1年高低点的位置

# TODO: MACD红柱拐点

# TODO: MACD绿柱拐点

# TODO: 多方炮

# TODO: 涨停基因

# TODO: 火焰三烧

# TODO: 强庄股

# TODO: 国家政策扶植

# TODO: 亏损超过3%则止损

# TODO: 破5日线，破10日线，破20日线止损

# TODO: 个股按生命线胜率评分，如：工商银行按20日生命线操作胜率达70%，得70分

# TODO: 根据个股检测指标的得胜率

import talib as tl
import numpy

# 初始化函数，设定要操作的股票、基准等等
def initialize(context):
    # 定义一个全局变量, 保存要操作的股票
    # 000001(股票:平安银行)
    g.security = '600218.XSHG'
    #设定沪深300作为基准
    set_benchmark('000001.XSHG')

# 每个单位时间(如果按天回测,则每天调用一次,如果按分钟,则每分钟调用一次)调用一次
def handle_data(context, data):
    # 获得当前时间
    hour = context.current_dt.hour
    minute = context.current_dt.minute
    if hour == 14 and minute == 59:
        macd(g.security)

# 获取MACD，含当前数据，适用于按分钟回测
def macd(security, fastperiod=12, slowperiod=26, signalperiod=9) :
    close = attribute_history(security, slowperiod*5, '1d', ('close'))['close'].values
    # 增加当日数据去计算
    cur_close = attribute_history(security, 1, '1m', ('close'))['close'].values
    close = numpy.concatenate((close,cur_close))
    #log.info('prices:', close)
    macdDIFF, macdDEA, macd = tl.MACDEXT(close, fastperiod=fastperiod, fastmatype=1, slowperiod=slowperiod, slowmatype=1, signalperiod=signalperiod, signalmatype=1)
    macd = macd * 2
    log.info("%s macd ==> DIFF=%s, DEA=%s, macd=%s", security, macdDIFF[-1], macdDEA[-1], macd[-1])
    return macdDIFF, macdDEA, macd

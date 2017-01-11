import utils

def initialize(context):
    g.security = '600218.XSHG'

def handle_data(context, data):
    hour = context.current_dt.hour
    minute = context.current_dt.minute
    if hour == 14 and minute == 59:
        # 测试移动平均线
        MA5 = utils.ma(g.security, 5)
        MA10 = utils.ma(g.security, 10)
        MA20 = utils.ma(g.security, 20)
        log.info("%s MA测试 ==> MA5=%s, MA10=%s, MA20=%s", g.security, f2(MA5), f2(MA10), f2(MA20))
        # 测试是否多头排列
        is_bull_market = utils.is_bull_market(g.security)
        log.info('%s 是否多头排列测试 ==> %s', g.security, is_bull_market)
        # 测试macd
        diff,dea,macd = utils.macd(g.security)
        log.info("%s MACD测试 ==> DIFF=%s, DEA=%s, MACD=%s", g.security, f2(diff[-1]), f2(dea[-1]), f2(macd[-1]))
        # 获取股票的位置,默认为近两年
        recent_gains, recent_decline = utils.stock_position(g.security)
        log.info("==> %s股票的位置：近期涨幅=%.2f，近期跌幅=%.2f", g.security, recent_gains, recent_decline)

def f2(value):
    return round(float(value), 2)

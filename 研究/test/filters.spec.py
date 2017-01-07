import filters

def initialize(context):
    g.stock_list = ['002659.XSHE','603389.XSHG','600495.XSHG','300585.XSHE',
                    '002199.XSHE','000155.XSHE']
    pass

def handle_data(context, data):
    hour = context.current_dt.hour
    minute = context.current_dt.minute
    if hour == 14 and minute == 59:
        # # 连接数据库
        # q = query(valuation.code)
        # # 按总市值升序排序，并取出前N个股票
        # q = q.order_by(
        #     valuation.market_cap.asc()
        # )
        # # 获取查询结果股票的财务数据
        # df = get_fundamentals(q)
        # # 获取查询结果所有股票的代码
        # stock_list = list(df['code'])
        stock_list = g.stock_list
        stock_list_length = len(stock_list)
        log.info("总股数=%s", stock_list_length)
        # 过滤创业板
        stock_list_gem = filters.gem(stock_list)
        log.info("创业板数量=%s", stock_list_length - len(stock_list_gem))
        # 过滤停牌股票
        stock_list_paused = filters.paused(stock_list)
        log.info("停牌股票数量=%s", stock_list_length - len(stock_list_paused))
        # 过滤ST及其他具有退市标签的股票
        stock_list_st = filters.st(stock_list)
        log.info("ST股票数量=%s", stock_list_length - len(stock_list_st))
        # 过滤涨停的股票
        stock_list_limitup = filters.limitup(context, stock_list)
        log.info("涨停股票数量=%s", stock_list_length - len(stock_list_limitup))
        # 过滤跌停的股票
        stock_list_limitdown = filters.limitdown(context, stock_list)
        log.info("跌停股票数量=%s", stock_list_length - len(stock_list_limitdown))

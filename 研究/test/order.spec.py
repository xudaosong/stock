import order


def initialize(context):  # 初始化函数，设定要操作的股票、基准等等.
    # 定义一个全局变量, 保存要操作的股票.
    g.security = '600218.XSHG'
    # 加载统计模块
    g.order = order.order()
    # 设定沪深300作为基准
    set_benchmark('000001.XSHG')


def handle_data(context, data):  # 每个单位时间(如果按天回测,则每天调用一次,如果按分钟,则每分钟调用一次)调用一次.
    #g.order.open_position(g.security, 100000)
    # log.info(context.portfolio.positions[g.security])
    # g.order.close_position(context.portfolio.positions[g.security])
    g.order.adjust_position(
        context, ['600218.XSHG', '601179.XSHG', '601117.XSHG'], 2)


def after_trading_end(context):  # 每天收盘后调用.
    #log.info("==> after trading end @ %s", str(context.current_dt))
    g.order.report(context)

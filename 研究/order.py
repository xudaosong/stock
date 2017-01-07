#coding=utf-8

from kuanke.user_space_api import *
import tradestat

class order():
    def __init__(self):
        # 加载统计模块
        self.trade_stat = tradestat.trade_stat()
        
    # 打印持仓报表
    def report(self, context):
        self.trade_stat.report(context)
    
    # 平仓，卖出指定持仓
    # 平仓成功并全部成交，返回True
    # 报单失败或者报单成功但被取消（此时成交量等于0），或者报单非全部成交，返回False
    def close_position(self, position):
        security = position.security
        order = order_target_value(security, 0) # 可能会因停牌失败
        if order != None:
            if order.filled > 0:
                # 只要有成交，无论全部成交还是部分成交，则统计盈亏
                self.trade_stat.watch(security, order.filled, position.avg_cost, position.price)
            if order.status == OrderStatus.held and order.filled == order.amount:
                # 全部成交
                return True
        return False

    # 开仓，买入指定价值的证券
    # 报单成功并成交（包括全部成交或部分成交，此时成交量大于0），返回True
    # 报单失败或者报单成功但被取消（此时成交量等于0），返回False
    def open_position(self, security, value):
        order = order_target_value(security, value)
        if order != None and order.filled > 0:
            # 报单成功并有成交
            return True
        return False

    # 仓位调整
    def adjust_position(self, context, buy_stocks, buy_stock_count):
        # 当前持股没有在买入的股票池则清仓
        for stock in context.portfolio.positions.keys():
            if stock not in buy_stocks:
                log.info("[%s] 股票清仓" %(stock))
                position = context.portfolio.positions[stock]
                self.close_position(position)
            else:
                log.info("[%s] 股票已经持仓" %(stock))
        # 根据股票数量分仓
        # 此处只根据可用金额平均分配购买，不能保证每个仓位平均分配
        position_count = len(context.portfolio.positions)
        if buy_stock_count > position_count:
            value = context.portfolio.cash / (buy_stock_count - position_count)

            for stock in buy_stocks:
                if context.portfolio.positions[stock].total_amount == 0:
                    if self.open_position(stock, value):
                        if len(context.portfolio.positions) == buy_stock_count:
                            break
    # 清空卖出所有持仓
    def clear_position(self, context):
        if context.portfolio.positions:
            log.info("==> 清仓，卖出所有股票")
            for stock in context.portfolio.positions.keys():
                position = context.portfolio.positions[stock]
                self.close_position(position)

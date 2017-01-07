#coding=utf-8

from kuanke.user_space_api import *

class filter_stock():
    # 过滤停牌股票
    def paused(self, stock_list):
        current_data = get_current_data()
        return [stock for stock in stock_list if not current_data[stock].paused]
    
    # 过滤ST及其他具有退市标签的股票
    def st(self, stock_list):
        current_data = get_current_data()
        return [stock for stock in stock_list 
            if not current_data[stock].is_st 
            and 'ST' not in current_data[stock].name 
            and '*' not in current_data[stock].name 
            and '退' not in current_data[stock].name]
    
    # 过滤涨停的股票,但不过滤已持仓的涨停股
    def limitup(self, context, stock_list):
        last_prices = history(1, unit='1m', field='close', security_list=stock_list)
        current_data = get_current_data()

        # 已存在于持仓的股票即使涨停也不过滤，避免此股票再次可买，但因被过滤而导致选择别的股票
        return [stock for stock in stock_list if stock in context.portfolio.positions.keys() 
            or last_prices[stock][-1] < current_data[stock].high_limit]
        #return [stock for stock in stock_list if stock in context.portfolio.positions.keys() 
        #    or last_prices[stock][-1] < current_data[stock].high_limit * 0.995]
        
    # 过滤跌停的股票
    def limitdown(self, context, stock_list):
        last_prices = history(1, unit='1m', field='close', security_list=stock_list)
        current_data = get_current_data()

        return [stock for stock in stock_list if stock in context.portfolio.positions.keys() 
            or last_prices[stock][-1] > current_data[stock].low_limit]
        #return [stock for stock in stock_list if last_prices[stock][-1] > current_data[stock].low_limit]
        #return [stock for stock in stock_list if stock in context.portfolio.positions.keys() 
        #    or last_prices[stock][-1] > current_data[stock].low_limit * 1.005]
        
    # 过滤创业版股票
    def gem(self, stock_list):
        return [stock for stock in stock_list if stock[0:3] != '300']

    # TODO:过滤最近两年亏损的股票
    
    # TODO:过滤被证监会谴责的股票
    
    #
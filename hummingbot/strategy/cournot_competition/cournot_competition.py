# -*- coding: utf-8 -*-
from decimal import Decimal
import logging
import pandas as pd
import numpy as np

from hummingbot.core.event.events import OrderType
from hummingbot.strategy.market_trading_pair_tuple import MarketTradingPairTuple
from hummingbot.logger import HummingbotLogger
from hummingbot.strategy.strategy_py_base import StrategyPyBase
from hummingbot.strategy.cournot_competition.cournot_competition_model import CournotCompetitionModel

from collections import deque


hws_logger = None


class CournotCompetitionStrategy(StrategyPyBase):
    # We use StrategyPyBase to inherit the structure. We also 
    # create a logger object before adding a constructor to the class. 
    @classmethod
    def logger(cls) -> HummingbotLogger:
        global hws_logger
        if hws_logger is None:
            hws_logger = logging.getLogger(__name__)
        return hws_logger

    def __init__(self,
                 market_info: MarketTradingPairTuple,
                 ):

        super().__init__()
        self._market_info = market_info
        self._connector_ready = False
        self._order_completed_buy = False
        self._order_completed_sell = False
        self.add_markets([market_info.market])
        self._model = CournotCompetitionModel()
        
    # After initializing the required variables, we define the tick method. 
    # The tick method is the entry point for the strategy. 
    def tick(self, timestamp: float):
        if not self._connector_ready:
            self._connector_ready = self._market_info.market.ready
            if not self._connector_ready:
                self.logger().warning(f"{self._market_info.market.name} is not ready. Please wait...")
                return
            else:
                self.logger().warning(f"{self._market_info.market.name} is ready. Trading started")

        if self._connector_ready:
            price_bid_1, quantity_bid_1, _ = list(next(self._market_info.order_book_bid_entries()))
            price_bid_2, quantity_bid_2, _  = list(next(self._market_info.order_book_bid_entries()))
            price_ask_1, quantity_ask_1, _ = list(next(self._market_info.order_book_ask_entries()))
            price_ask_2, quantity_ask_2, _ = list(next(self._market_info.order_book_ask_entries()))
            
            spread = np.log(float(price_ask_1)) - np.log(float(price_bid_1))
            price = np.log(float(self._market_info.get_mid_price()))
            quantity = float(quantity_bid_1) * 1000.
                        
            #self.logger().info((spread, price, quantity))
            
            quantity_first_seller = float(quantity_bid_1)
            quantity_second_seller = float(quantity_bid_2)
            cost_first_seller = float(price) - np.log(float(price_bid_1))
            cost_second_seller = float(price) -np.log(float(price_bid_2))
            
            params = {'price':float(price), 
                      'quantity':float(quantity), 
                      'spread': float(spread), 
                      'quantity_first_seller': float(quantity_first_seller), 
                      'quantity_second_seller': float(quantity_second_seller), 
                      'cost_first_seller': float(cost_first_seller), 
                      'cost_second_seller': float(cost_second_seller)}
            result = self._model.update(params)
            self.logger().info(pd.DataFrame([result]).T)
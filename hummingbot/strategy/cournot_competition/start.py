# -*- coding: utf-8 -*-
from hummingbot.strategy.market_trading_pair_tuple import MarketTradingPairTuple
from hummingbot.strategy.cournot_competition import CournotCompetitionStrategy
from hummingbot.strategy.cournot_competition.cournot_competition_config_map import cournot_competition_config_map as c_map

def start(self):
    connector = c_map.get("connector").value.lower()
    market = c_map.get("market").value

    self._initialize_markets([(connector, [market])])
    base, quote = market.split("-")
    market_info = MarketTradingPairTuple(self.markets[connector], market, base, quote)
    self.market_trading_pair_tuples = [market_info]
    self.strategy = CournotCompetitionStrategy(market_info)

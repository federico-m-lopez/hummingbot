# -*- coding: utf-8 -*-

from hummingbot.client.config.config_var import ConfigVar

# Returns a market prompt that incorporates the connector value set by the user
def market_prompt() -> str:
    connector = cournot_competition_config_map.get("connector").value
    return f'Enter the token trading pair on {connector} >>> '

# List of parameters defined by the strategy
cournot_competition_config_map ={
    "strategy":
        ConfigVar(key="strategy",
                  prompt="",
                  default="cournot_competition",
    ),
    "connector":
        ConfigVar(key="connector",
                  prompt="Enter the name of the exchange >>> ",
                  prompt_on_new=True,
    ),
    "market": ConfigVar(
        key="market",
        prompt=market_prompt,
        prompt_on_new=True,
    ),
}
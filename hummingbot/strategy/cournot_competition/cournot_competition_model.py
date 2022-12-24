from collections import deque
from river.linear_model import BayesianLinearRegression
from river.preprocessing import  StandardScaler


class CournotCompetitionModel:
    
    # price: This is the price of the good or asset.
    # quantity: This is the quantity of the good or asset.
    # alpha: This is the intercept of the demand curve. It represents the maximum quantity of the good or asset that buyers are willing to purchase at a price of 0.
    # beta: This is the slope of the demand curve. It represents the rate at which the quantity demanded decreases as the price increases.
    # cost: This is the cost of producing a unit of the good or asset.
    # quantity_first_seller: This is the quantity of the good or asset supplied by the first seller.
    # quantity_second_seller: This is the quantity of the good or asset supplied by the second seller.
    # cost_first_seller: This is the cost of producing a unit of the good or asset for the first seller.
    # cost_second_seller: This is the cost of producing a unit of the good or asset for the second seller.
    
    def __init__(self, **kwargs) -> None:
        self.alpha = None
        self.beta = None
        self.model = ( StandardScaler() | BayesianLinearRegression() )
    
    
    def update(self, kwargs):
        self.price = kwargs.get('price')
        self.quantity =  kwargs.get('quantity')
        self.cost =  kwargs.get('spread')/ 2.
        self.quantity_first_seller = kwargs.get('quantity_first_seller')
        self.quantity_second_seller = kwargs.get('quantity_second_seller')
        self.cost_first_seller = kwargs.get('cost_first_seller')
        self.cost_second_seller = kwargs.get('cost_second_seller')
        
        #linear regression to figure out market demand
        x={"0": self.price}
        y=self.quantity
        result = self.model.learn_one(x, y).predict_one(x, as_dist=True)
        self.alpha = result.mu
        self.beta = result.sigma
                
        #independent                
        self.calculate_cost()
        self.calculate_profit()
        self.calculate_total_quantity()
        self.calculate_market_supply()
        
        #depends on linear regression        
        self.calculate_demand()
        self.calculate_market_price()
        self.calculate_market_quantity()
        self.calculate_market_demand()
        self.calculate_inverse_demand()
        self.calculate_inverse_supply()
        self.calculate_inverse_market_supply()
        self.calculate_inverse_market_demand()
        
        return self.to_dict()
        
    # define the demand function
    def calculate_demand(self):
        if self.alpha is not None and self.beta is not None:
            self.demand = self.alpha - self.beta*self.price

    # define the cost function for each seller
    def calculate_cost(self):
        self.cost = self.cost * self.quantity

    # define the profit function for each seller
    def calculate_profit(self):
        self.profit =  self.price * self.quantity -  self.cost * self.quantity

    # define the total quantity function
    def calculate_total_quantity(self):
        self.total_quantity =  self.quantity_first_seller +  self.quantity_second_seller

    # define the market price function
    def calculate_market_price(self):
        if self.alpha is not None and self.beta is not None:
            self.market_price = (self.alpha - self.quantity_first_seller - self.quantity_second_seller)/self.beta

    # define the market quantity function
    def calculate_market_quantity(self):
        if self.alpha is not None and self.beta is not None:
            self.market_quantity = self.alpha - self.beta * self.price

    # define the market demand function
    def calculate_market_demand(self):
        if self.alpha is not None and self.beta is not None:
            self.market_demand = self.beta * self.price

    # define the market supply function
    def calculate_market_supply(self):
        self.market_supply = self.quantity_first_seller + self.quantity_second_seller

    # define the inverse demand function
    def calculate_inverse_demand(self):
        if self.alpha is not None and self.beta is not None:
            self.inverse_demand = (self.alpha - self.quantity)/self.beta

    # define the inverse supply function
    def calculate_inverse_supply(self):
        self.inverse_suppy = self.cost/self.price

    # define the inverse market demand function
    def calculate_inverse_market_demand(self):
        if self.alpha is not None and self.beta is not None:
            self.inverse_market_demand = (self.alpha - self.quantity)/self.beta

    # define the inverse market supply function
    def calculate_inverse_market_supply(self):
        self.inverse_market_supply = (self.cost_first_seller + self.cost_second_seller)/self.price
            
    # def to_dict(self):
    #     attrs = [ i for i in dir(self) if "__" not in i ]
    #     values = [ getattr(self, i) for i in attrs if getattr(self, i) is not callable ]
    #     return dict(zip(attrs, values))
    
    def to_dict(self):
        return {'alpha':self.alpha, 'beta':self.beta, 'price': self.price, 'demand': self.demand, 'cost': self.cost, 'quantity': self.quantity, 'profit': self.profit,
                'total_quantity': self.total_quantity,'market_price': self.market_price, 'market_quantity': self.market_quantity,
                'market_demand': self.market_demand,  'market_supply': self.market_supply, 'inverse_demand': self.inverse_demand,'inverse_suppy': self.inverse_suppy,'inverse_market_demand': self.inverse_market_demand,'inverse_market_supply': self.inverse_market_supply,}
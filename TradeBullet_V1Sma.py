import backtrader as bt

class OptimizedSMACrossover(bt.Strategy):
    params = (
        ('short_sma_period', 14),
        ('long_sma_period', 28),
        ('risk_per_trade', 0.4),
        ('stop_loss', 1.5)
    )

    def __init__(self):
        self.short_sma = bt.indicators.SMA(period=self.params.short_sma_period)
        self.long_sma = bt.indicators.SMA(period=self.params.long_sma_period)
        self.crossover = bt.indicators.CrossOver(self.short_sma, self.long_sma)

    def next(self):
        if self.position.size == 0:
            if self.crossover > 0:  # A buy signal
                risk_per_unit = self.params.stop_loss * self.data._name
                account_risk = self.broker.getvalue() * self.params.risk_per_trade
                qty = account_risk / risk_per_unit
                self.buy(size=int(qty))
            elif self.crossover < 0:  # A sell signal
                risk_per_unit = self.params.stop_loss * self.data._name
                account_risk = self.broker.getvalue() * self.params.risk_per_trade
                qty = account_risk / risk_per_unit
                self.sell(size=int(qty))

        else:
            # exit logic 
            if self.position.size > 0 and self.crossover < 0:
                self.close()  # Close long position
            elif self.position.size < 0 and self.crossover > 0:
                self.close()  # Close short position


# Cerebro entity
cerebro = bt.Cerebro(initialcash=500)

# strategy
cerebro.addstrategy(OptimizedSMACrossover)

# data feed
# cerebro.adddata(data)

# desired cash
cerebro.broker.setcash(500)

# commission - 0.1% ... divide by 100 to remove the %
cerebro.broker.setcommission(commission=0.001)

# Run over everything
strategies = cerebro.run()
final_value = cerebro.broker.getvalue()
print(f'Final Portfolio Value: {final_value}')

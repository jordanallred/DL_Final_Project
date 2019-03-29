from Predictions import rf_predict
from numpy import reshape, shape
from time import sleep

trading_strategy = {
    'purchase percentage': 0.50
}

def simulate_decisions(trading_strategy: dict, principal: int, prices: list, times: list, decisions: list):
    balance = principal
    print(len(prices) // 12)
    if len(prices) != len(decisions) or len(decisions) != len(times) or len(prices) != len(times):
        print("Lists not of equal length")
        print(len(prices))
        print(len(decisions))
        print(len(times))
        exit(-1)
    days = len(prices) // 390
    remainder = len(prices) % 390
    prices = prices[remainder:]
    prices = reshape(prices, (days, 390, 1))
    decisions = decisions[remainder:]
    times = times[remainder:]
    trading_log = []
    for day_index in range(len(prices)):
        purchase_power = trading_strategy['purchase percentage'] * balance
        total_shares = 0
        day = prices[day_index]
        for minute_index in range(len(day)):
            minute = day[minute_index]
            price = minute[0]
            decision = decisions[day_index * 390 + minute_index]
            time = times[day_index * 390 + minute_index]
            if len(trading_log) > 0:
                if trading_log[-1]['action'] == 'buy' and trading_log[-1]['time'] < time:
                    action = 'sell'
                    shares = trading_log[-1]['shares']
                    balance += shares * price
                    total_shares -= shares
                    purchase = {
                        'time': time,
                        'shares': shares,
                        'price': price,
                        'action': action,
                        'total shares': total_shares,
                        'balance': balance
                    }
                    trading_log.append(purchase)
            if decision == 1 and purchase_power > price:
                action = 'buy'
                if balance < purchase_power:
                    shares = balance // price
                else:
                    shares = purchase_power // price
                balance -= shares * price
                total_shares += shares
            else:
                shares = 0
                action = 'null'
            purchase = {
                'time': time,
                'shares': shares,
                'price': price,
                'action': action,
                'total shares': total_shares,
                'balance': balance
            }
            if action != 'null':
                trading_log.append(purchase)
            if time > 1558 and total_shares > 0:
                action = 'sell'
                shares = trading_log[-1]['shares']
                balance += shares * price
                total_shares -= shares
                purchase = {
                    'time': time,
                    'shares': shares,
                    'price': price,
                    'action': action,
                    'total shares': total_shares,
                    'balance': balance
                }
                trading_log.append(purchase)
        if total_shares > 0:
            print("Total Shares: " + str(total_shares))
            exit(-1)
        print(balance)
        # print(trading_log)
        trading_log.clear()


prices, times, decisions = rf_predict('amazon')
simulate_decisions(trading_strategy, 5000, prices, times, decisions)

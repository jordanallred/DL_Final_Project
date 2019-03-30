from Predictions import rf_predict
from numpy import reshape, shape
from os import listdir
from Data_Utils import stocks_dict

trading_strategy = {
    'daily percentage': 0.50,
    'purchase percentage': 0.50
}

stocks_file = "C:\\Users\\Jordan Allred\\Documents\\Deep Learning Final Project\\Augmented Dataset\\"


def simulate_decisions_individual(company_name: str, trading_strategy: dict, principal: int, monthly_payments: int):
    prices, times, decisions = rf_predict(company_name, verbose=True)
    balance = principal
    six_month = principal
    total_investment = principal
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
    minutes_traded = 0
    for day_index in range(len(prices)):
        daily_balance = trading_strategy['daily percentage'] * balance
        balance -= daily_balance
        purchase_power = trading_strategy['purchase percentage'] * daily_balance
        total_shares = 0
        day = prices[day_index]
        for minute_index in range(len(day)):
            minutes_traded += 1
            minute = day[minute_index]
            price = minute[0]
            decision = decisions[day_index * 390 + minute_index]
            time = times[day_index * 390 + minute_index]
            if len(trading_log) > 0:
                if trading_log[-1]['action'] == 'buy' and trading_log[-1]['time'] < time:
                    action = 'sell'
                    shares = trading_log[-1]['shares']
                    daily_balance += shares * price
                    total_shares -= shares
                    purchase = {
                        'time': time,
                        'shares': shares,
                        'price': price,
                        'action': action,
                        'total shares': total_shares,
                        'daily balance': daily_balance
                    }
                    trading_log.append(purchase)
            if decision == 1 and purchase_power > price:
                action = 'buy'
                if balance < purchase_power:
                    shares = daily_balance // price
                else:
                    shares = purchase_power // price
                daily_balance -= shares * price
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
                'daily balance': daily_balance
            }
            if action != 'null':
                trading_log.append(purchase)
            if time > 1558 and total_shares > 0:
                action = 'sell'
                shares = trading_log[-1]['shares']
                daily_balance += shares * price
                total_shares -= shares
                purchase = {
                    'time': time,
                    'shares': shares,
                    'price': price,
                    'action': action,
                    'total shares': total_shares,
                    'daily balance': daily_balance
                }
                trading_log.append(purchase)
            if (minutes_traded + 1) % 6783 == 0:
                print("Monthly return: $" + str(int(round(balance - six_month))))
                print("Monthly return rate: " + str(int(round(100 * balance / six_month))) + "%\n")
                balance += monthly_payments
                total_investment += monthly_payments
                six_month = balance
        if total_shares > 0:
            print("Total Shares: " + str(total_shares))
            exit(-1)
        balance += daily_balance
        # print(balance)
        # print(trading_log)
        trading_log.clear()
    print("Total Investment: $" + str(total_investment))
    print("Return: $" + str(int(round(balance))))


def simulate_decisions_all(trading_strategy: dict, principal: int, monthly_payments: int):
    trade_data = []
    for company in listdir(stocks_file):
        prices, times, decisions = rf_predict(company)
        if len(prices) != len(decisions) or len(decisions) != len(times) or len(prices) != len(times):
            print("Lists not of equal length")
            print(len(prices))
            print(len(decisions))
            print(len(times))
            exit(-1)
        company_data = {
            'company name': company,
            'prices': prices,
            'times': times,
            'decisions': decisions,
            'total shares': 0,
            'trade log': []
        }
        trade_data.append(company_data)
    balance = principal
    six_month = principal
    total_investment = principal

    length = len(trade_data[0]['prices'])
    days = length // 390
    remainder = length % 390

    for company in trade_data:
        if len(company['prices']) != length:
            print("Lists of unequal length for company: " + company['company name'])
            exit(-1)
        else:
            company['prices'] = company['prices'][remainder:]
            company['times'] = company['times'][remainder:]
            company['decisions'] = company['decisions'][remainder:]

    minutes_traded = 0
    for day in range(days):
        daily_balance = trading_strategy['daily percentage'] * balance
        purchase_power = trading_strategy['purchase percentage'] * daily_balance
        for minute in range(390):
            minutes_traded += 1
            for company in trade_data:
                try:
                    price = company['prices'][day * 390 + minute]
                except IndexError:
                    print(day * 390 + minute)
                    print(len(company['prices']))
                    print(len(company['times']))
                    print(len(company['decisions']))
                    print(days * 390)
                    exit(-1)
                decision = company['decisions'][day * 390 + minute]
                time = company['times'][day * 390 + minute]
                trading_log = company['trade log']
                total_shares = company['total shares']
                if len(trading_log) > 0:
                    if trading_log[-1]['action'] == 'buy' and trading_log[-1]['time'] < time:
                        action = 'sell'
                        shares = trading_log[-1]['shares']
                        daily_balance += shares * price
                        total_shares -= shares
                        purchase = {
                            'time': time,
                            'shares': shares,
                            'price': price,
                            'action': action,
                            'total shares': total_shares,
                            'daily balance': daily_balance
                        }
                        trading_log.append(purchase)
                if decision == 1 and purchase_power > price:
                    action = 'buy'
                    if daily_balance < purchase_power:
                        shares = daily_balance // price
                    else:
                        shares = purchase_power // price
                    daily_balance -= shares * price
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
                    'daily balance': daily_balance
                }
                if action != 'null':
                    trading_log.append(purchase)
                if time > 1558 and total_shares > 0:
                    action = 'sell'
                    shares = trading_log[-1]['shares']
                    daily_balance += shares * price
                    total_shares -= shares
                    purchase = {
                        'time': time,
                        'shares': shares,
                        'price': price,
                        'action': action,
                        'total shares': total_shares,
                        'daily balance': daily_balance
                    }
                    trading_log.append(purchase)
            if (minutes_traded + 1) % 6783 == 0:
                print("Monthly return: $" + str(int(round(balance - six_month))))
                print("Monthly return rate: " + str(int(round(100 * balance / six_month))) + "%\n")
                balance += monthly_payments
                six_month = balance
                total_investment += monthly_payments
        balance += daily_balance - trading_strategy['daily percentage'] * balance

    print("Total Investment: $" + str(total_investment))
    print("Return: $" + str(int(round(balance))))


# simulate_decisions_all(trading_strategy, 200, 50)
for key in list(stocks_dict.keys()):
    simulate_decisions_individual(stocks_dict[key], trading_strategy, 1000, 50)

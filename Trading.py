from Predictions import rf_predict, rf_predict_live_data, lstm_predict_live_data
from numpy import reshape
from os import listdir
# from Data_Utils import stocks_dict

trading_strategy = {
    'daily percentage': 0.50,
    'purchase percentage': 0.50
}

stocks_file = "C:\\Users\\Jordan Allred\\Documents\\Deep Learning Final Project\\Alternative Dataset - Volume\\"


def simulate_decisions_individual(company_name: str, trading_strategy: dict, principal: int, monthly_payments: int):
    prices, times, decisions, accuracy = rf_predict(company_name, verbose=False, train_size=0.01)
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
        trading_log.clear()
    print("Total Investment: $" + str(total_investment))
    print("Return: $" + str(int(round(balance))))


def simulate_decisions_individual_live(company_name: str, trading_strategy: dict, principal: int, monthly_payments: int):
    prices, times, decisions, accuracy = rf_predict_live_data(company_name, verbose=False)
    print(accuracy)
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
        trading_log.clear()
    print("Total Investment: $" + str(total_investment))
    print("Return: $" + str(int(round(balance))))


def simulate_decisions_all(trading_strategy: dict, principal: int, monthly_payments: int):
    trade_data = []
    for company in listdir(stocks_file):
        prices, times, decisions, accuracy = rf_predict(company, train_size=0.01, verbose=False)
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

    for company in trade_data:
        if len(company['prices']) < length:
            length = len(company['prices'])
    days = length // 390
    remainder = length % 390

    for company in trade_data:
        company['prices'] = company['prices'][remainder:length]
        company['times'] = company['times'][remainder:length]
        company['decisions'] = company['decisions'][remainder:length]

    minutes_traded = 0
    monthly_average = 0
    months = 0
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
                monthly_average = (monthly_average * months + int(round(100 * balance / six_month))) / (months + 1)
                months += 1
                balance += monthly_payments
                six_month = balance
                total_investment += monthly_payments
        balance += daily_balance - trading_strategy['daily percentage'] * balance

    print("Total Investment: $" + str(total_investment))
    print("Return: $" + str(int(round(balance))))
    print("Average Monthly Return Rate: " + str(monthly_average))


simulate_decisions_all(trading_strategy, 5000, 100)

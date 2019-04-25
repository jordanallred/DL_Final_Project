from alpha_vantage.timeseries import TimeSeries
from Data_Utils import stocks_dict
from Data_Utils import write_csv
from os import listdir, mkdir, remove, removedirs
from os.path import isdir
from Data_Utils import read_csv, add_column, identify_extrema
from shutil import copy
# from time import sleep

stocks_file = "C:\\Users\\Jordan Allred\\Documents\\Deep Learning Final Project\\Live Data\\"
download_file = "C:\\Users\\Jordan Allred\\Documents\\Deep Learning Final Project\\Live Data Download\\"


def stockchart(symbol):
    ts = TimeSeries(key='OCI3XR8QL7DH46XS', output_format='pandas', retries=100)
    data, meta_data = ts.get_intraday(symbol=symbol, interval='1min', outputsize='full')
    date = []
    time = []
    for info in data.axes[0]:
        date.append(info.split(' ')[0])
        time.append(str(int(info.split(' ')[1][:-2].replace(':', '')) - 1))
    close = list(data['4. close'])
    volume = list(data['5. volume'])
    write_data = [['Date', 'Time', 'Price', 'Volume']]
    check_date = date[0]
    for index in range(len(date)):
        if date[index] != check_date:
            if len(write_data) == 391:
                if not isdir(download_file):
                    mkdir(download_file)

                if not isdir(download_file + stocks_dict[symbol]):
                    mkdir(download_file + stocks_dict[symbol])

                write_csv(download_file + stocks_dict[symbol] + "\\" +
                          check_date.replace('-', '_') + ".csv", write_data)
            write_data.clear()
            write_data.append(['Date', 'Time', 'Price', 'Volume'])
            write_data.append([check_date.replace('-', ''), time[index].strip(':'),
                               str(close[index]), str(volume[index])])
            check_date = date[index]
        else:
            write_data.append([check_date.replace('-', ''), time[index].strip(':'),
                               str(close[index]), str(volume[index])])


def download_live_stocks(max_tries = 10):
    failure = True
    stock_keys = list(stocks_dict.keys())
    tries = 0
    while failure:
        failure = False
        remove_keys = []
        for symbol in stock_keys:
            download = True
            try:
                stockchart(symbol)
            except KeyError:
                download = False
                failure = True
                continue
            finally:
                if download:
                    remove_keys.append(symbol)
                print("Downloading " + symbol.upper() + (" successful" if download else " failed"))
        for to_remove in remove_keys:
            stock_keys.remove(to_remove)
        tries += 1
        if tries == max_tries:
            break

    add_percent_change(1)
    add_percent_change(5)
    add_percent_change(15)
    add_percent_change(30)
    add_percent_change(60)
    add_decisions()
    for directory in listdir(download_file):
        for file in listdir(download_file + directory):
            copy(download_file + directory + "\\" + file, stocks_file + directory + "\\" + file)
            remove(download_file + directory + "\\" + file)
        removedirs(download_file + directory)


def add_percent_change(minutes: int):
    company_directory = listdir(download_file)
    for company in company_directory:
        day_directory = listdir(download_file + company)
        for day in day_directory:
            day_dataset = read_csv(download_file + company + "\\" + day)
            price_index = -1
            for line in day_dataset:
                if str(line).__contains__('Price'):
                    price_index = line.index('Price')
                if price_index < 0:
                    print('check for price')
                    exit(-1)
            change_list = []
            change_list += [str(0)] * minutes
            for index in range(1 + minutes, len(day_dataset)):
                percent_change = 100 * ((float(day_dataset[index][price_index]) -
                                         float(day_dataset[index - minutes][price_index])) /
                                        float(day_dataset[index - minutes][price_index]))
                change_list.append(str(percent_change))
            add_column(str(minutes) + "-minute Percent Change", change_list, download_file + company + "\\" + day)


def add_decisions():
    for company in listdir(download_file):
        for day in listdir(download_file + company):
            maxima_x, maxima_y, minima_x, minima_y, length, prices = \
                identify_extrema(download_file + company + '\\' + day, 2, 0)
            decisions = []
            for point in range(length):
                if minima_x.__contains__(point):
                    decisions.append('buy')
                elif maxima_x.__contains__(point):
                    decisions.append('sell')
                else:
                    decisions.append('hold')

            buy, sell, hold = [], [], []
            buy_x, sell_x, hold_x = [], [], []
            for price in range(len(prices)):
                point = prices[price]
                if decisions[price] is 'buy':
                    buy.append(float(point))
                    buy_x.append(price)
                elif decisions[price] is 'sell':
                    sell.append(float(point))
                    sell_x.append(price)
                elif decisions[price] is 'hold':
                    hold.append(float(point))
                    hold_x.append(price)
                else:
                    print('Problem with decisions. Check array.')
                    exit(-1)
            add_column('Decision', decisions, download_file + company + '\\' + day)

download_live_stocks()

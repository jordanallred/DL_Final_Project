from alpha_vantage.timeseries import TimeSeries
from Data_Utils import stocks_dict
from Data_Utils import write_csv

stocks_file = "C:\\Users\\Jordan Allred\\Documents\\Deep Learning Final Project\\Live Data\\"

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
                write_csv(stocks_file + stocks_dict[symbol] + "\\" + check_date.replace('-', '_') + ".csv", write_data)
            write_data.clear()
            write_data.append(['Date', 'Time', 'Price', 'Volume'])
            write_data.append([check_date.replace('-', ''), time[index].strip(':'), str(close[index]), str(volume[index])])
            check_date = date[index]
        else:
            write_data.append([check_date.replace('-', ''), time[index].strip(':'), str(close[index]), str(volume[index])])


stock_keys = list(stocks_dict.keys())
for symbol in stock_keys:
    print(symbol)
    stockchart(symbol)

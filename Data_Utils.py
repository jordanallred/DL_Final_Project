from os import listdir
from os import remove
from os.path import isdir, isfile
from os import mkdir
from shutil import copy
from csv import reader
from matplotlib import pyplot as plt
from numpy import arange, ceil, shape, array, reshape

stocks_dict = {
    'aapl': 'apple',
    'bac': 'bank of america',
    # 'f': 'ford',
    'fb': 'facebook',
    'ge': 'general electric',
    # 'goog': 'google',
    'amzn': 'amazon',
    'intc': 'intel',
    'msft': 'microsoft',
    't': 'att'
}

stocks_file = "C:\\Users\\Jordan Allred\\Documents\\Deep Learning Final Project\\Alternative Dataset\\"
live_data_file = "C:\\Users\\Jordan Allred\\Documents\\Deep Learning Final Project\\Live Data - Volume\\"


def delete_experimental_files():
    day_directory = listdir(stocks_file)

    for day in day_directory:
        all_files = listdir(stocks_file + day)
        for file in all_files:
            if file.__contains__('experimental'):
                remove(stocks_file + day + "\\" + file)


def sort_files_by_company():
    day_directory = listdir(stocks_file)

    for day in day_directory:
        all_files = listdir(stocks_file + day)
        for file in all_files:
            company = stocks_dict[file.replace('.csv', '')]
            if not isdir(stocks_file + company):
                mkdir(stocks_file + company)
            copy(stocks_file + day + "\\" + file, stocks_file + company + "\\" + day + '.csv')


def write_stock_headers():
    company_directory = listdir(stocks_file)

    for company in company_directory:
        day_directory = listdir(stocks_file + company)
        for day in day_directory:
            temporary = 'C:\\Users\\Jordan Allred\\Documents\\Deep Learning Final Project\\temporary.csv'
            with open(stocks_file + company + "\\" + day, 'r') as open_file:
                csv_reader = reader(open_file)
                with open(temporary, 'w+') as write_file:
                    # write_data = [['Date', 'Time', 'Open', 'High', 'Low', 'Close', 'Volume', 'Split', 'Earnings', 'Dividends']]
                    write_data = [['Time', 'Date', 'Price', 'Volume']]

                    for line in csv_reader:
                        if 'Time' in line:
                            write_data = []
                        write_data.append(line)
            remove(stocks_file + company + "\\" + day)
            write_csv(stocks_file + company + "\\" + day, write_data)
            remove(temporary)


def write_csv(file: str, data: list):
    final_data = ""
    for line in data:
        for point in line:
            if line.index(point) is 0:
                final_data += point
            else:
                final_data += (',' + point)
        final_data += ('\n')
    with open(file, 'w+') as open_file:
        open_file.write(final_data)


def read_csv(file: str):
    with open(file, 'r') as open_file:
        csv_reader = reader(open_file)
        write_data = []
        for line in csv_reader:
            write_data.append(line)
    return write_data


def remove_column(name: str):
    company_directory = listdir(stocks_file)

    for company in company_directory:
        day_directory = listdir(stocks_file + company)
        for day in day_directory:
            print(company + "\\" + day)
            with open(stocks_file + company + "\\" + day, 'r') as open_file:
                csv_reader = reader(open_file)
                write_data = []
                header_to_remove = -1
                for line in csv_reader:
                    if str(line).__contains__('Date'):
                        # header_to_remove = line.index(name, -1)
                        header_to_remove = line.index(name)
                    if header_to_remove < 0:
                        print('not a legal header name')
                        exit(-1)
                    write_data.append(line[:header_to_remove] + line[header_to_remove + 1:])
            write_csv(stocks_file + company + "\\" + day, write_data)


def add_column(name: str, data: list, file: str):
    with open(file, 'r') as open_file:
        write_data = []
        csv_reader = reader(open_file)
        csv_length = 0
        reader_index = 0
        for line in csv_reader:
            if csv_length is 0:
                write_data.append(line + [name])
            else:
                write_data.append(line + [data[reader_index]])
                reader_index += 1
            csv_length += 1

    if len(data) != csv_length - 1:

        print('INCORRECT DATA SIZE:')
        print('csv length is ' + str(csv_length - 1))
        print('data input length is ' + str(len(data)))
        print('csv length must match data input length')
        exit(-1)

    write_csv(file, write_data)


def add_percent_change(minutes: int):
    company_directory = listdir(stocks_file)
    for company in company_directory:
        day_directory = listdir(stocks_file + company)
        for day in day_directory:
            print(company + "\\" + day)
            day_dataset = read_csv(stocks_file + company + "\\" + day)
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
                percent_change = 100 * ((float(day_dataset[index][price_index]) - float(day_dataset[index - minutes][price_index])) / float(day_dataset[index - minutes][price_index]))
                change_list.append(str(percent_change))
            add_column(str(minutes) + "-minute Percent Change", change_list, stocks_file + company + "\\" + day)


def change_header_name(original: str, new: str):
    company_directory = listdir(stocks_file)
    for company in company_directory:
        day_directory = listdir(stocks_file + company)
        for day in day_directory:
            day_dataset = read_csv(stocks_file + company + "\\" + day)
            day_dataset[0][day_dataset[0].index(original)] = new
            write_csv(stocks_file + company + "\\" + day, day_dataset)


def display_day(file: str):
    day_dataset = read_csv(file)

    price_index = -1
    line = day_dataset[0]
    if str(line).__contains__('Price'):
        price_index = line.index('Price')
        titles = line[price_index:]
    if price_index < 0:
        print('check for price')
        exit(-1)
    plot_data = []
    for minute in day_dataset[1:]:
        plot_data.append(minute[price_index:])
    for category in range(len(titles)):
        plot_y = []
        plot_sum = 0
        for data_point in plot_data:
            plot_y.append(float(data_point[category]))
            plot_sum += float(data_point[category])
        average = plot_sum / len(plot_data)
        plt.subplot(ceil(len(titles) / 2), 2, category + 1)
        plt.plot(arange(0, len(plot_y)), plot_y)
        plt.legend([titles[category]])
        if min(plot_y) < 0:
            plt.plot(arange(0, len(plot_y)), [0] * len(plot_y), dashes=[4, 2])
            plt.legend([titles[category]] + ['Zero'])
        plt.yticks(arange((min(plot_y)), (max(plot_y)), step=((max(plot_y) - min(plot_y)) / 5 - 0.01)))
    plt.show()


def display_price(file: str, per_minute: int):
    day_dataset = read_csv(file)

    price_index = -1
    line = day_dataset[0]
    if str(line).__contains__('Price'):
        price_index = line.index('Price')
        titles = line[price_index:]
    if price_index < 0:
        print('check for price')
        exit(-1)
    plot_data = []
    for minute in day_dataset[1:]:
        plot_data.append(minute[price_index])
    plot_y = []
    plot_x = []
    plot_sum = 0
    for data_point in range(len(plot_data)):
        if data_point % per_minute is 0:
            plot_x.append(data_point)
            plot_y.append(float(plot_data[data_point]) + 0)
            plot_sum += float(plot_data[data_point])
    average = plot_sum / len(plot_data)
    plt.pause(1)
    plt.plot(plot_x, plot_y)
    plt.legend(['Price'])
    plt.yticks(arange((min(plot_y)), (max(plot_y)), step=((max(plot_y) - min(plot_y)) / 5 - 0.01)))
    plt.show()
    return plot_x, plot_y


def identify_extrema(file: str, minutes: int, verbose: int):
    day_dataset = read_csv(file)

    price_index = -1
    line = day_dataset[0]
    if str(line).__contains__('Price'):
        price_index = line.index('Price')
        titles = line[price_index:]
    if price_index < 0:
        print('check for price')
        exit(-1)
    plot_data = []
    for minute in day_dataset[1:]:
        plot_data.append(minute[price_index])
    plot_y = []
    plot_x = []
    for data_point in range(len(plot_data)):
        plot_x.append(data_point)
        plot_y.append(float(plot_data[data_point]))

    maxima_x, minima_x, maxima_y, minima_y = [], [], [], []
    for point in range(len(plot_y) - minutes):
        extrema = 'undetermined'
        for neighbors in range(minutes):
            if extrema is 'undetermined':
                if plot_y[point] < plot_y[point + 1]:
                    extrema = 'increasing'
                elif plot_y[point] > plot_y[point + 1]:
                    extrema = 'decreasing'
                else:
                    break
            else:
                if extrema is 'increasing' and plot_y[point + neighbors] >= plot_y[point + neighbors + 1]:
                    extrema = 'undetermined'
                    break
                if extrema is 'decreasing' and plot_y[point + neighbors] <= plot_y[point + neighbors + 1]:
                    extrema = 'undetermined'
                    break
        if extrema is 'increasing':
            minima_x.append(plot_x[point + minutes // 2])
            minima_y.append(plot_y[point + minutes // 2])
        if extrema is 'decreasing':
            maxima_x.append(plot_x[point + minutes // 2])
            maxima_y.append(plot_y[point + minutes // 2])

    plt.scatter(maxima_x, maxima_y, color='r')
    plt.scatter(minima_x, minima_y, color='g')
    plt.plot(plot_x, plot_y)

    if verbose > 0:
        plt.show()

    return maxima_x, maxima_y, minima_x, minima_y, len(day_dataset) - 1, plot_data


def add_decisions():
    for company in listdir(stocks_file):
        for day in listdir(stocks_file + company):
            maxima_x, maxima_y, minima_x, minima_y, length, prices = identify_extrema(stocks_file + company + '\\' + day, 2, 0)
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
            add_column('Decision', decisions, stocks_file + company + '\\' + day)
            print(stocks_file + company + '\\' + day)


def get_dataset(company_name: str):
    company_directory = stocks_file + company_name + "\\"
    company_files = listdir(company_directory)
    dataset = []
    for file in company_files:
        data = read_csv(company_directory + file)[1:]
        for index in range(len(data)):
            line = data[index]
            if line[-1] == 'sell':
                data[index][-1] = '-1'
            elif line[-1] == 'hold':
                data[index][-1] = '0'
            elif line[-1] == 'buy':
                data[index][-1] = '1'
            dataset.append(line)
    return dataset


def get_test_dataset(company_name: str):
    company_directory = live_data_file + company_name + "\\"
    company_files = listdir(company_directory)
    dataset = []
    for file in company_files:
        data = read_csv(company_directory + file)[1:]
        for index in range(len(data)):
            line = data[index]
            if line[-1] == 'sell':
                data[index][-1] = '-1'
            elif line[-1] == 'hold':
                data[index][-1] = '0'
            elif line[-1] == 'buy':
                data[index][-1] = '1'
            dataset.append(line)
    return dataset


def get_split_dataset_all():
    dataset = []
    for company in listdir(stocks_file):
        dataset.append(get_split_dataset_individual(company))


def get_split_dataset_individual(company_name: str):
    dataset = get_dataset(company_name)
    features, labels = [], []
    for data in dataset:
        features.append([float(number) for number in data[:-1]])
        labels.append(int(data[-1]))
    return features, labels


def get_split_live_dataset_individual(company_name: str):
    dataset = get_test_dataset(company_name)
    features, labels = [], []
    for data in dataset:
        try:
            features.append([float(number) for number in data[:-1]])
        except:
            print(data)
        labels.append(int(data[-1]))
    return features, labels


def LSTM_data_prep(X_train, y_train, X_test, y_test):
    return reshape(array(X_train), (shape(X_train)[0], shape(X_train)[1], 1)), reshape(array(y_train), (shape(y_train)[0], 1)), reshape(array(X_test), (shape(X_test)[0], shape(X_test)[1], 1)), reshape(array(y_test), (shape(y_test)[0], 1))


def CNN_data_prep(company_name: str):
    features, labels = get_split_dataset_individual(company_name)
    CNN_features, CNN_labels = [], []
    feature_dataset, label_dataset = [], []
    day = 0
    minute = 0.0
    day_index = 0
    for index in range(len(features)):
        feature = features[index]
        if day == 0:
            day = feature[0]
        if feature[0] == day:
            feature_dataset.append(feature[1:])
            label_dataset.append([labels[index]])
            minute += 1
        else:
            if 0 < len(feature_dataset) < 390:
                difference = 390 - len(feature_dataset)
                for diff in range(difference):
                    feature_dataset.append([0] * 8)
                    label_dataset.append([labels[index]])

            minute = 0.0

            CNN_features.append(feature_dataset)
            CNN_labels.append(label_dataset)
            feature_dataset.clear()
            label_dataset.clear()
            feature_dataset.append(feature[1:])
            label_dataset.append([labels[index]])
            day = feature[0]

    return array(CNN_features), array(CNN_labels)


def CNN_live_data_prep(company_name: str):
    features, labels = get_split_live_dataset_individual(company_name)
    CNN_features, CNN_labels = [], []
    feature_dataset, label_dataset = [], []
    day = 0
    minute = 0.0
    day_index = 0
    for index in range(len(features)):
        feature = features[index]
        if day == 0:
            day = feature[0]
        if feature[0] == day:
            feature_dataset.append(feature[1:])
            label_dataset.append([labels[index]])
            minute += 1
        else:
            if 0 < len(feature_dataset) < 390:
                difference = 390 - len(feature_dataset)
                for diff in range(difference):
                    feature_dataset.append([0] * 8)
                    label_dataset.append([labels[index]])

            minute = 0.0

            CNN_features.append(feature_dataset)
            CNN_labels.append(label_dataset)
            feature_dataset.clear()
            label_dataset.clear()
            feature_dataset.append(feature[1:])
            label_dataset.append([labels[index]])
            day = feature[0]

    return array(CNN_features), array(CNN_labels)


def change_time_format():
    company_directory = listdir(stocks_file)
    for company in company_directory:
        day_directory = listdir(stocks_file + company)
        for day in day_directory:
            print(company + "\\" + day)
            day_dataset = read_csv(stocks_file + company + "\\" + day)
            time_index = -1
            time = 0
            for line in day_dataset:
                if str(line).__contains__('Time'):
                    time_index = line.index('Time')
                if time_index < 0:
                    print('check for time')
                    exit(-1)
                if time > 0:
                    line[time_index] = str(time - 1)
                time += 1
            write_csv(stocks_file + company + "\\" + day, day_dataset)
    change_header_name('Time', 'Minutes Since Open')


def split_by_day():
    company_directory = listdir(stocks_file)
    for company in company_directory:
        if not isdir(stocks_file + company):
            mkdir(stocks_file + company)
        for file in listdir(stocks_file + company):
            day_data = []
            current_day = ""
            data = read_csv(stocks_file + company + "\\" + file)
            date_index = -1
            for line in data:
                if date_index > -1 and line != []:
                    date = line[date_index].split(' ')[0]
                    time = line[date_index].split(' ')[1]
                    del line[date_index]
                    line.insert(date_index, date)
                    line.insert(date_index, time)
                    file_name = date.replace('.', '_')
                    if current_day == "":
                        current_day = date
                    if date != current_day:
                        if len(day_data) == 390:
                            if not isfile(stocks_file + company + "\\" + file_name):
                                print(company + "\\" + file_name)
                                write_csv(stocks_file + company + "\\" + file_name + ".csv", day_data)
                        day_data.clear()
                        day_data.append(line)
                        current_day = date
                    else:
                        day_data.append(line)

                if str(line).__contains__('Date'):
                    date_index = line.index('Date')
                if date_index < 0:
                    print('check for date')
                    exit(-1)


def switch_columns(column1: str, column2: str):
    company_directory = listdir(stocks_file)
    for company in company_directory:
        if not isdir(stocks_file + company):
            mkdir(stocks_file + company)
        for file in listdir(stocks_file + company):
            day_data = []
            column1_index, column2_index = -1, -1
            data = read_csv(stocks_file + company + "\\" + file)
            for line in data:
                if str(line).__contains__('Date'):
                    column1_index = line.index(column1)
                    column2_index = line.index(column2)
                if column1_index < 0:
                    print('check for ' + column1)
                    exit(-1)
                if column2_index < 0:
                    print('check for ' + column2)
                    exit(-1)
                print(line)
                new_column1 = line[column2_index]
                new_column2 = line[column1_index]

                while new_column1.__contains__('.'):
                    new_column1 = new_column1.replace('.', '')
                    # print(new_column1)

                while new_column2.__contains__('.'):
                    new_column2 = new_column2.replace('.', '')
                    # print(new_column2)

                del line[column1_index]
                if new_column1.__contains__('.'):
                    break
                line.insert(column1_index, new_column1)

                del line[column2_index]
                if new_column1.__contains__('.'):
                    break
                line.insert(column2_index, new_column2)
                print(line)
                day_data.append(line)
            write_csv(stocks_file + company + "\\" + file, day_data)


def get_data_points():
    company_directory = listdir(stocks_file)
    for company_name in company_directory:
        points = 0
        for file in listdir(stocks_file + company_name):
            data = read_csv(stocks_file + company_name + "\\" + file)
            for line in data:
                if not str(line).__contains__('Date'):
                    points += 1
        print(company_name + ": " + "{:,}".format(points) + " data points")


import csv
import statistics

#go through stocks see which one follows DJI most closely
#also keep track of how it over / underperforms on avg
#choose next stock by how it over or underperforms on avg, to blance out previous stock
#do this until you have n number of stocks
#for each we should have avg value, avg value of stock / DJI value, trend vs DJI num, 

#now, to weight the chosen stocks. we'll take into account the avg stock value, its trend vs DJI, and weight vs DJI

def index_maker(n, index_name, history):

    #First we'll collect the data into dictionaries. The histories will be stored in lists, because the order of days is important.
    #stocks variable will be a dictionary with sub-dictionaries, corresponding to each stock.
    index = dict()
    index['history'] = list()
    stocks= dict()

    with open(history, newline='') as csvfile:
        #open CSV file with module to read contents
        reader = csv.reader(csvfile)

        #skip the header
        next(reader)

        for row in reader:
            name = row[0]
            date = row[1]
            value = float(row[2])
            if name == index_name:
                index['history'].append(tuple([date,value]))
            else:
                if not stocks.get(name):
                    stocks[name] = dict()
                    stocks[name]['history'] = list() 

                stocks[name]['history'].append(tuple([date,value]))

    #now we have grabbed what we need from the CSV, we will crunch some numbers for each stock in linear O(n) time
    index['avg'] = statistics.mean([price for date, price in index['history']])

    #this function will give us an array that tells us the relative differences between prices day to day, so if
    #day 1 to day 2 the DJI increased by 1% we'd see [1.01...]
    def get_difs(arr):
        result = list()
        #we check up until the last date so offset -1
        for i in range(0, len(arr) - 1):
            price = arr[i][1]
            next_day_price = arr[i+1][1]
            delta = next_day_price / price
            result.append(delta)
        return result
    
    index['dif'] = get_difs(index['history'])
    
    #now get analyze the data for each stock, comparing it to the index
    for stock_name in stocks:
        stock = stocks[stock_name]

        #this tells us how the stock price progression relatively mirrors the index rating,
        # the closer to a stocks avg_dif is to 0, the closer it follows the index's trend 
        stock_dif = get_difs(stock['history'])
        relative_dif = [index['dif'][ind] - dif for ind,dif in enumerate(stock_dif)]
        avg_relative_dif = statistics.mean(relative_dif)
        stock['avg_relative_dif'] = avg_relative_dif

        #we'll get the stock's average
        stock['avg_price'] = statistics.mean([price for date, price in stock['history']])
    
    #now we have the data necessary to select the stocks that will best represent the index
    #we will want stocks that perform near the index for avg_relative_dif, and be sure there is a mix of stocks that perform above and below the index on avg
    stock_difs = [{'stock_name': stock_name, 'stock_dif': stock_data['avg_relative_dif'], 'stock_avg':stock_data['avg_price']} for stock_name, stock_data in stocks.items()]
    chosen_stocks = list()
    current_rel = 0

    # print(stock_difs)

    #this loop selects n stocks from our stock difs list based on how close they keep the current_rel variable to 0
    #keeping this variable near 0 tells us that the average change in all the stocks is close to the avg change in the index over time
    while len(chosen_stocks) < n:
        optimal_rel = 0 - current_rel
        best_ind = None
        best_dif = 100000000

        for ind,stock in enumerate(stock_difs):
            stock_opt_rel_dif = abs(optimal_rel - stock['stock_dif'])
            if stock_opt_rel_dif < best_dif:
                best_dif = stock_opt_rel_dif
                best_ind = ind 
        best_stock = stock_difs.pop(best_ind)
        chosen_stocks.append(best_stock)
        current_rel += best_stock['stock_dif']
    
    # print(chosen_stocks)
    # print(sum([el['stock_dif'] for el in chosen_stocks]))
    
    #we'll want each stock to represent 1/n of the weight of the index's average
    share_value = index['avg'] / n
    for stock in chosen_stocks:
        stock['shares'] = int(share_value / stock['stock_avg'])
    print(chosen_stocks)

    print(sum([stock['shares'] * stocks[stock['stock_name']]['history'][0][1] for stock in chosen_stocks]))



    




index_maker(5, '.DJI', 'dow_jones_historical_prices.csv')
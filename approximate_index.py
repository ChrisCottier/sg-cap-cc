import csv
import statistics
import sys

def index_maker(n, index_name, history):

    #First we'll collect the data into dictionaries. The histories for the index/stocks will be stored in lists, because the order of days is important for my algorithm implementaion.
    #Note: I chose the word stock over security as I am more familiar with the term.
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

    #now we have grabbed what we need from the CSV, we will crunch some numbers for the index, and each stock, in linear O(n) time
    index['avg'] = statistics.mean([price for date, price in index['history']])

    #this function will give us an array that tells us the relative differences between index or stock value day to day, so if
    #day 1 to day 2 the DJI increased by 1% we'd see [1.01,...]
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
    #we will want stocks that perform near the index for avg_relative_dif, and be sure there is a mix of stocks that perform above and below the index on average
    stock_difs = [{'stock_name': stock_name, 'stock_dif': stock_data['avg_relative_dif'], 'stock_avg':stock_data['avg_price']} for stock_name, stock_data in stocks.items()]
    chosen_stocks = list()
    current_rel = 0


    #this loop selects n stocks from our stock difs list based on how close they keep the current_rel variable to 0
    #each selection of a stock will change current_rel by its deviation from the index 
    #keeping this variable near 0 tells us that the average change in all the stocks is close to the avg change in the index over time
    while len(chosen_stocks) < n:
        optimal_rel = 0 - current_rel
        best_ind = None
        best_dif = 100000000

        #Here we iterate through the stock options, choosing the one that whose relative difference from the index is closest to the optimal rel variable.
        for ind,stock in enumerate(stock_difs):
            stock_opt_rel_dif = abs(optimal_rel - stock['stock_dif'])
            if stock_opt_rel_dif < best_dif:
                best_dif = stock_opt_rel_dif
                best_ind = ind 
        best_stock = stock_difs.pop(best_ind)
        chosen_stocks.append(best_stock)
        current_rel += best_stock['stock_dif']
    
    
    #for my algorithm to work, we'll want each stock to represent 1/n of the value of the index's average, so we'll calculate the weight of that stock accordingly
    target_stock_value = index['avg'] / n
    for stock in chosen_stocks:
        #the shares of each stock will be rounded to 3 decimal places, per the .CHIDOG example in implementation details
        stock['weight'] = round(target_stock_value / stock['stock_avg'], 3)


    #we'll print the results, so they may be outputted into a new CSV
    print('Symbol',',' ,'Weight')
    for stock in chosen_stocks:
        print(stock['stock_name'],',', stock['weight'])
    return


    
n = sys.argv[1]
index_name = sys.argv[2]
history = sys.argv[3]

#this is the function call whenever the python script is invoked. 
#the arguments for this function are defined above; they are the command line arguments
index_maker(int(n), index_name, history)

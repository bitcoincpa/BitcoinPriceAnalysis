import requests

from datetime import datetime, timedelta
dt = datetime.today()
import pandas as pd
from decimal import *

cp = requests.get('https://api.coindesk.com/v1/bpi/currentprice.json')
hp = requests.get('https://api.coindesk.com/v1/bpi/historical/close.json?start=2011-01-01&end=2019-06-05')

# --- Pandas Frequency Rate for List of Dates
frequency = {'Week (Sunday)':'W-SUN', 'Week (Monday)':'W-MON', 'Week (Tuesday)': 'W-TUE', 'Week (Wednesday)': 'W-WED',\
                'Week (Thursday)': 'W-THU', 'Week (Friday)':'W-FRI', 'Week (Saturday)': 'W-SAT', 'Month-End': 'M', 'Daily': 'D', 'Quarter-End' : 'Q'}

# --- Print Current BTC Price
#print("The current price of Bitcoin is " + cp.json()['bpi']['USD']['rate'])
current_price = cp.json()['bpi']['USD']['rate_float']
#print(current_price)

#print("Current date: {}".format(dt.now())
current_time = str(dt.year) + "-" + str(dt.month) + "-" + str(dt.day-1)
#print(current_time)

start_date = input('Enter the start date: (YYYY-MM-DD) : ' )
freq = input('How frequently did you want to invest: ')
amt = int(input('How much did you want to spend per {}: '.format(freq)))



def listofdates(start_date, current_time, freq):
    
#--- Creates list of dates based on start date and frequency inputs.
    return pd.date_range(start_date,current_time, 
            freq=frequency[freq]).strftime("%Y-%m-%d").tolist()
    

dates = listofdates(start_date,current_time,freq)

#--- Calculate how much BTC would have been purchased per frequency and amount inpuyts.
total_btc = 0
total_spent=0
for date in dates:
    price =  hp.json()['bpi'][date]
    btc = amt/price
    total_spent +=amt
    total_btc += btc
    
    print("The price of Bitcoin on {} was {}. You would have bought {} BTC.".format(date,price,btc))
    
    
#-- Analysis
average = total_spent / total_btc
total_worth = total_btc * current_price
total_gain = total_worth - total_spent

print("If you spent ${} on BTC every {} from {} to {}, you would have {} BTC worth {}. \nTotal Cost: {} \nTotal Gain/(Loss): {} ".format(amt,freq,dates[0], dates[-1], total_btc,total_worth, total_spent, total_gain))

    



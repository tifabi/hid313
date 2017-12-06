'''
Collect Historical Stock Data
Tiffany Fabianac Modified code from:
    - http://pandas-datareader.readthedocs.io/en/latest/remote_data.html
'''

from pandas_datareader import data
import pandas as pd
import csv
import string
import datetime
from collections import defaultdict
from pandas.tseries.offsets import BDay


def stockData (startDate, endDate, ticker):
	# Define which online source one should use
	data_source = 'google'

	# User pandas_reader.data.DataReader to load the desired data.
	panel_data = data.DataReader(ticker, data_source, startDate, endDate)

	close = panel_data.ix['Close']
	volume = panel_data.ix['Volume']
	op = panel_data.ix['Open']
	high = panel_data.ix['High']
	low = panel_data.ix['Low']

	# Getting all weekdays between 01/01/2017 and 12/31/2017
	all_weekdays = pd.date_range(start=startDate, end=endDate, freq='B')

	# Align new set of dates
	close = close.reindex(all_weekdays)
	volume = volume.reindex(all_weekdays)
	op = op.reindex(all_weekdays)
	high = high.reindex(all_weekdays)
	low = low.reindex(all_weekdays)

	result = pd.concat([close, volume, op, high, low], axis=1, join='inner')
	result.columns=['close','volume','open','high','low']
	return result
	
    
def findHigh (startDate, ticker):

	# Get date and five days after
	temp_date = datetime.datetime.strptime(startDate, "%Y-%m-%d")
	endDate = temp_date + BDay(5)

	
	result = stockData(startDate, endDate, ticker)
	tempHigh = result.nlargest(1,'high')
	high = tempHigh.iloc[0]['high']
	return high

def openPrice (startDate, ticker):
	temp_date = datetime.datetime.strptime(startDate, "%Y-%m-%d")
	endDate = temp_date + BDay(1)

	result = stockData(startDate, endDate, ticker)
	open = result.iloc[0]['open']
	return open

with open('google_alert_data.csv', 'rb') as csvfile:
	with open('labeledTrainData.csv','wb') as f:
		datareader = csv.DictReader(csvfile)
		writer = csv.DictWriter(f, fieldnames=datareader.fieldnames, extrasaction='ignore', delimiter=',', skipinitialspace=True)
		writer.writeheader()
		for line in datareader:
			if (line['Ticker'] == ''):
				pass
			elif (line['Snippit'] == ''):
				pass
			else:
				ticker = [line['Ticker']]
				date = line['Date']
				high = findHigh(date, ticker)
				startPrice = openPrice(date, ticker)
				prctIncrease = round(((high-startPrice)/startPrice)*100,2)
				if (high > startPrice*1.1):
					line['W/L?']='W'
					line['%Change']=prctIncrease
					print ticker, prctIncrease, high, startPrice, date
				else:
					line['W/L?']='L'
					line['%Change']=prctIncrease
				line['Snippit'] = line['Snippit'].replace(',', '')
				writer.writerow(line)


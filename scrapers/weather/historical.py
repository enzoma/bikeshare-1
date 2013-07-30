import os
import json
import urllib2
import time
import unicodecsv as csv
import datetime
from forecastio import forecastio 
import psycopg2

city_lat  = 42.3587
city_long = -71.0567

try:
  conn = psycopg2.connect("dbname="+os.environ.get('dbname')+" user="+os.environ.get('dbuser')+ " host="+os.environ.get('dburl'))
except:
  print "I am unable to connect to the database"
  exit()
cur = conn.cursor()

#Casts float from string when the is the posbility of the empty string
def add_zero(item):
  if (item == 0 or item == "None" or item == ""):
    return 0.0
  else:
    return item

forecast = forecastio.Forecastio(str(os.environ.get('FORECASTIOKEY')))
result = forecast.load_forecast(city_lat,city_long)

start_date = datetime.datetime(2010,1,2)
end_date = datetime.datetime(2013,7,30)
d = start_date
delta = datetime.timedelta(hours=1)

myfile = open('weather_data_boston_2.csv', 'wb')
wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
header_list = ["time","summary","precipIntensity","precipProbability","precipType","precipAccumulation","temperature"]
wr.writerow(header_list)

while d <= end_date:
    print d
    result = forecast.load_forecast(city_lat,city_long,d,lazy=True)
    current = forecast.get_currently()
    days_list = []
    item = current
    time = item.time
    summary = item.summary
    precip_intensity = item.precipIntensity
    precip_probility = item.precipProbability
    precip_type = item.precipType
    precip_accumulation = item.precipAccumulation
    temperature = item.temperature
    cur.execute("""INSERT INTO weather_boston (time,summary,precipIntensity,precipProbability,precipType,precipAccumulation,temperature) VALUES
        (%s,%s,%s,%s,%s,%s,%s);""",
        (time,summary,precip_intensity,precip_probility,precip_type,precip_accumulation,temperature))
    d += delta

conn.commit()


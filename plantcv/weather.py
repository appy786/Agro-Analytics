import requests
import pandas as pd
import urllib, json


def weather_data(lt,ln):
	coord_API_endpoint = "http://api.openweathermap.org/data/2.5/weather?"
	lat_long = "lat=" + str(lt)+ "&lon=" + str(ln)
	join_key = "&appid=" + "d60bc3c136024472c4b560deb96acd60"
	units = "&units=metric"

	current_coord_weather_url= coord_API_endpoint + lat_long + join_key + units
	#print(current_coord_weather_url)

	json_data = requests.get(current_coord_weather_url).json()
	#print(json_data)
	llt=str(round(lt,6))
	lln=str(round(ln,6))

	coord_API_endpoint = "https://opendata-download-metfcst.smhi.se/api/category/fwif1g/version/1/daily/geotype/point"
	lat_long = "/lon/" + lln  + "/lat/" + llt
	join_key = "/data.json"


	url= coord_API_endpoint + lat_long + join_key 
	#print(url)
	r = requests.get(url)
	j_data= r.json()
	#print(j_data)


	df  = pd.DataFrame()

	# Create empty lists to store the JSON Data
	prediction_num=0
	fwi_value = []
	ffmc_value = []
	bui_value =[]
	dmc_value=[]
	dc_value=[]
	isi_value=[]
	current_weather_id = []
	current_time = []
	own_city_id = []
	city = []
	latitude = []
	longitude = []
	country = []
	timezone = []
	temp = []
	pressure = []
	humidity = []
	ws_value = []
	rain_value=[]
	prec_value=[]

	current_time.append(pd.Timestamp.now())
	own_city_id.append(json_data['id'])
	city.append(json_data['name'])
	latitude.append(llt)
	longitude.append(lln)
	country.append(json_data['sys']['country'])
	fwi_value.append(j_data['timeSeries'][0]['parameters'][1]['values'])
	ffmc_value.append(j_data['timeSeries'][0]['parameters'][4]['values'])
	bui_value.append(j_data['timeSeries'][0]['parameters'][3]['values'])
	dmc_value.append(j_data['timeSeries'][0]['parameters'][5]['values'])
	dc_value.append(j_data['timeSeries'][0]['parameters'][6]['values'])
	isi_value.append(j_data['timeSeries'][0]['parameters'][2]['values'])
	temp.append(j_data['timeSeries'][0]['parameters'][8]['values'])
	ws_value.append(j_data['timeSeries'][0]['parameters'][10]['values'])
	rain_value.append(j_data['timeSeries'][0]['parameters'][11]['values'])
	prec_value.append(j_data['timeSeries'][0]['parameters'][12]['values'])

	df['current_time'] = current_time
	df['own_city_id'] = own_city_id
	df['city'] = city
	df['latitude'] = latitude
	df['longitude'] = longitude
	df['country'] = country
	df['fwi'] = fwi_value
	df['bui'] = bui_value
	df['ffmc'] = ffmc_value
	df['dmc']=dmc_value
	df['dc']=dc_value
	df['isi']=isi_value
	df['temp']=temp
	df['ws']=ws_value
	df['r']=rain_value
	df['prec']=prec_value


	print(df.head())

	with open('main1.csv', 'a') as f:
	    df.to_csv(f, header=False,index=False)





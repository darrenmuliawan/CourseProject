import requests
import json
import urllib.parse
import codecs

API_KEY = 'AIzaSyDH6j8kqZHQEx5Z0H9KSWzpUweIKKl3CpI'

def main(uni_path,location_path):
	with open(uni_path,'r') as f:
		unis = f.readlines()

	unis = [uni.strip() for uni in unis]

	base_url = 'https://maps.googleapis.com/maps/api/place/'
	place_url = 'findplacefromtext/json?'
	place_params = {'fields':'place_id','key':API_KEY,'inputtype':'textquery'}

	detail_url = 'details/json?'
	details_params = {'fields':'address_components','key':API_KEY}
	countries = []
	states = []
	uni_states = {}
	uni_countries = {}

	for uni in unis:
		try:
			state =uni_states[uni]
			country = uni_countries[uni]
		except KeyError:

			place_params['input'] = uni 
			url = base_url+place_url+urllib.parse.urlencode(place_params)
			# print (url)
			resp = requests.get(url)
			place_id = None
			try:
				place_id = json.loads(resp.text)['candidates'][0]['place_id']
			except:
				print (uni)
				state = ''
				country = ''
				uni_states[uni] = state
				uni_countries[uni] = country
			if place_id:
				details_params['place_id'] = place_id
				url = base_url+detail_url+urllib.parse.urlencode(details_params)
				resp = requests.get(url)
				resp_json = json.loads(resp.text)
				comps = resp_json['result']['address_components']
				found_state = False
				found_country = False
				print(comps,uni)
				for comp in comps:
					if len(comp['types'])>1:
						if comp['types'][0]=='administrative_area_level_1':
							state = comp['long_name']
							uni_states[uni] = state 
							found_state = True
						if comp['types'][0]=='country':
							country = comp['long_name']
							uni_countries[uni] = country
							found_country = True
				if not found_state:
					state = country
				if not found_country:
					print (uni,"no country")

		states.append(state)
		countries.append(country)


	with codecs.open(location_path,'w',encoding='utf-8',errors='ignore') as f:
		for i,c in enumerate(countries[:-1]):
			f.write(states[i]+'\t'+c+'\n') 
		f.write(states[-1]+'\t'+countries[-1]) 

if __name__ == '__main__':
	main('../data/unis','../data/location')

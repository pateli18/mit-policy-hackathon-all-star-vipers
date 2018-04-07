import requests, os, datetime, json

def format_points(point_list):
	point_string = ""
	for point in point_list:
		formatted_point = f'{point[0]},{point[1]}|'
		point_string += formatted_point
	return point_string[:-1]

def format_time(target_time):
	epoch = datetime.datetime(1970,1,1)
	departure_time = int((target_time - epoch).total_seconds())
	return departure_time

def generate_request(origins, destinations, departure_time, mode):
	url = 'https://maps.googleapis.com/maps/api/distancematrix/json?'
	origins = format_points(origins)
	destinations = format_points(destinations)
	departure_time = format_time(departure_time)
	data = {'origins' : origins, 'departure_time':str(departure_time),
	'destinations': destinations,'key':os.environ["GOOGLE_API_KEY"], 'mode':mode}
	return url, data

def process_response(origins, destinations, response_data):
	all_data = []
	for i, origin in enumerate(origins):
		elements = response_data["rows"][i]["elements"]
		for j, destination in enumerate(destinations):
			individual_data = {"origin": {"geocode":origin, "address":response_data["origin_addresses"][i]},
							  "destination":{"geocode":destination, "address":response_data["destination_addresses"][j]},
							  "distance":elements[j]["distance"], "duration":elements[j]["duration"],
							  "duration_in_traffic":elements[j]["duration_in_traffic"]}
			all_data.append(individual_data)
	return all_data

def get_response(origins, destinations, target_time, mode):
	url, data = generate_request(origins, destinations,target_time, mode)
	try:
		response = requests.get(url, params = data)
		response_data = json.loads(response.text)
		output = process_response(origins, destinations, response_data)
	except:
		output = None
	return output


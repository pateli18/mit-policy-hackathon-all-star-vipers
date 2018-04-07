import datetime, json, argparse
from google_time_distance_api import get_response
import pandas as pd

def generate_date_list(start_day = 1, end_day = 7, start_time = 5, end_time = 22, months = [3, 6, 9, 12], year = 2018):
	date_list = []
	for month in months:
		for day in range(start_day, end_day + 1):
			actual_year = year
			if datetime.datetime(year, month, day) < datetime.datetime.today():
				actual_year = year + 1
			for time in range(start_time, end_time + 1):
				date_list.append(datetime.datetime(actual_year, month, day, time))
	return date_list

def get_data(base_point, input_filepath, output_filepath, mode = "driving"):
	df_target_points = pd.read_csv(input_filepath)
	target_points = [(row["lat"], row["lng"]) for _, row in df_target_points.iterrows()]
	base_point = [base_point]
	
	all_data = {}

	dates = generate_date_list()
	for i, date in enumerate(dates):
		key = date.strftime("%Y-%m-%d %H")
		all_data[key] = {}
		all_data[key]["to"] = get_response(target_points, base_point, date, mode)
		all_data[key]["from"] = get_response(base_point, target_points, date, mode)
		if i % 10 == 0:
			print(f'{i} out of {len(dates)} complete...')

	json.dump(all_data, open(output_filepath, "w"))

if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument('-i', '--inputfilepath', nargs = 1, type = str)
	parser.add_argument('-o', '--outputfilepath', nargs = 1, type = str)
	parser.add_argument('-m', '--mode', nargs = '?', type = str, default = "driving")

	base_point = (42.349327,-71.041791)

	args = parser.parse_args()
	params = {}
	params["base_point"] = base_point
	params["input_filepath"] = args.inputfilepath[0]
	params["output_filepath"] = args.outputfilepath[0]
	params["mode"] = args.mode

	get_data(**params)
		


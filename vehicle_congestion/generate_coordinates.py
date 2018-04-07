import pandas as pd
import math, argparse, os

def get_new_lat_lng(base, degree, distance):
	distance_m = 1609.34 * distance
	east_displacement = distance_m * math.sin(2 * math.pi / (360 / degree)) / (math.cos(2 * math.pi / (360 / base[0]))) / 111111
	north_displacement = distance_m * math.cos(2 * math.pi / (360 / degree)) / 111111
	return (base[0] + north_displacement, base[1] + east_displacement, distance)

def generate_points(base_point, minimum, increment, maximum, output_filepath):
	all_coordinates = []
	for distance in range(minimum, maximum, increment):
		distance /= 100
		num_degrees = int(distance / .5 * 2)
		for degree in range(1, num_degrees + 1):
			degree *= (360 / num_degrees) 
			all_coordinates.append(get_new_lat_lng(base_point, degree, distance))
	df = pd.DataFrame(all_coordinates, columns=['lat', 'lng', 'distance'])
	df.to_csv(output_filepath, index = False)

if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument('-i', '--increment', nargs = '?', type = int, default = 50)
	parser.add_argument('-mn', '--min', nargs = '?', type = int, default = 750)
	parser.add_argument('-mx', '--max', nargs = '?', type = int, default = 800)
	parser.add_argument('-o', '--outputfilepath', nargs = 1, type = str)

	base_point = (42.349327,-71.041791)

	args = parser.parse_args()
	params = {}
	params["base_point"] = base_point
	params["minimum"] = args.min
	params["maximum"] = args.max
	params["increment"] = args.increment
	params["output_filepath"] = args.outputfilepath[0]

	generate_points(**params)
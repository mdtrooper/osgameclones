#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
from getopt import *
import json
import pystache

# Debug
from pprint import *

def help():
	print("Converter list games in json to github markdown.\n")
	print("Usage:")
	print("\t -o <file>, --output <file> \t Set the output file")
	print("\t -t <file>, --template <file> \t Set the template file (in mustache syntax)")
	print("\t -d <file>, --data <file> \t Set the data file (in json syntax)")
	print("\t -h, --help \t\t\t Show this help")

def mardown_anchor_link(text):
	return_var = text
	
	return_var = return_var.lower()
	return_var.replace(" ", "-")
	return_var.replace(" ", "-")
	return_var.replace("/", "")
	return_var = "#" + return_var
	
	return return_var

def mardown_anchor_anchor(text):
	return_var = text
	
	return_var = return_var.lower()
	return_var.replace(" ", "-")
	return_var.replace(" ", "-")
	return_var.replace("/", "")
	return_var.replace(u"™", "")
	return_var = "<a name=\"" + return_var + "\"></a>"
	
	return return_var

def get_categories(data):
	categories = set()
	
	for game in data['games']:
		categories.add(game['category'])
	
	categories = list(categories)
	
	return categories

def get_systems(data):
	systems = set()
	
	for game in data['games']:
		systems.add(game['system'])
	
	systems = list(systems)
	
	return systems

def is_any_game_with_category_and_system(data, category, system):
	return_var = False
	
	for game in data['games']:
		if game['category'] == category and game['system'] == system:
			return_var = True
			break
	
	return return_var

def get_sort_games(data, system, category):
	return_var = []
	
	for game in data['games']:
		if game['category'] == category and game['system'] == system:
			item = {}
			item['title'] = game['title']
			item['description'] = game['description']
			item['repository'] = game['repository']
			if 'play_it_now' in game:
				item['play_it_now'] = game['play_it_now']
			
			if not return_var:
				return_var.append(item)
			else:
				inserted = False
				for index, value in enumerate(return_var):
					if value['title'] > item['title']:
						return_var.insert(index - 1, item)
						inserted = True
						break
				
				if not inserted:
					return_var.append(item)
	
	return return_var

def main():
	try:
		options, args = getopt(sys.argv[1:], 'o:t:d:h', \
			['output=', 'template=', 'data=', 'help'])
	except GetoptError as err:
		print("[FAIL] " + err)
		help()
		sys.exit(2)
	
	output_file = None
	template_file = None
	data_file = None
	if args:
		data_file = args[0]
	
	for opt, val in options:
		if opt in ("-h", "--help"):
			help()
			sys.exit(0)
		
		if opt in ("-o", "--output"):
			output_file = val
		elif opt in ("-t", "--template"):
			template_file = val
		elif opt in ("-d", "--data"):
			data_file = val
	
	if (not template_file) or (not data_file):
		print("[FAIL] Template files is not setted and data file is not setted.")
		help()
		exit(1)
	
	print("[INFO] Starting to parse the data file.")
	
	json_data=open(data_file)
	try:
		data = json.load(json_data)
	except ValueError as err:
		print("[FAIL] There is a error in the data file (%s)." % data_file)
		print err
		exit(1)
	
	categories = get_categories(data)
	categories.sort()
	systems = get_systems(data)
	systems.sort()
	
	print("[INFO] Making the intermediate json for the mustache template.")
	intermediate_json = {}
	intermediate_json['toc'] = []
	intermediate_json['list_system'] = []
	for system in systems:
		item = {}
		item['system'] = system
		item['mardown_anchor_link(system)'] = mardown_anchor_link(system)
		item['category_toc'] = []
		
		item_a = {}
		item_a['system'] = system
		item_a['mardown_anchor_anchor(system)'] = mardown_anchor_anchor(system)
		item_a['list_category'] = []
		
		for category in categories:
			if is_any_game_with_category_and_system(data, category, system):
				item_2 = {}
				item_2['category'] = category
				item_2['mardown_anchor_link(category)'] = mardown_anchor_link(system + category)
				item['category_toc'].append(item_2)
				
				item_2_a = {}
				item_2_a['category'] = category
				item_2_a['mardown_anchor_anchor(category)'] = mardown_anchor_anchor(system + category)
				item_2_a['games'] = []
				item_2_a['games'] = get_sort_games(data, system, category)
				
				item_a['list_category'].append(item_2_a)
		
		intermediate_json['toc'].append(item)
		intermediate_json['list_system'].append(item_a)
	
	
	pprint(intermediate_json)
	
	print("[INFO] Render the template.")
	
	renderer = pystache.Renderer()
	output = renderer.render_path(template_file, intermediate_json)
	
	if output_file:
		text_file = open(output_file, "w")
		text_file.write(output)
		text_file.close()
	else:
		print output 

if __name__ == "__main__":
	main()
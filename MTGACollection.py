from mtga.set_data import all_mtga_cards
from pathlib import Path
import requests
import json

def get_set_data(code):
	"""Return set data based on set code from Scryfall."""
	info = requests.get(r"https://api.scryfall.com/sets/" + code)
	return info.json()

directory = r"C:\Program Files\Wizards of the Coast\MTGA\MTGA_Data\Logs\Logs"
file = sorted(Path(directory).iterdir(), reverse=True)[0]

with open(file, "r", encoding="utf-8-sig") as log_file:
	lines = log_file.readlines()
	
	for line in lines:
		if "<== PlayerInventory.GetPlayerCards" in line:
			data = line
			break

	for char in data:
		if char == "{":
			data = data[data.index(char):]
			break

	collection_data = json.loads(data)


set_codes = ["GRN", "RNA", "WAR", "M20", "ELD", "THB", "IKO", "M21", "AKR"]
sets = dict()

for code in set_codes:
	info = get_set_data(code)
	sets[code] = {"owned_cards": 5, "total_cards": info['card_count']}

for key, value in collection_data['payload'].items():
	card = all_mtga_cards.find_one(key)
	# No need to keep track of basic lands...
	if card.pretty_name in ['Plains', 'Island', 'Swamp', 'Mountain', 'Forest']:
		continue
	else:
		print("Name: {}, Set: {}, Amount: {}".format(card.pretty_name, card.set, value))

		if card.set.upper() in set_codes:
			sets[card.set.upper()]['owned_cards'] += 1

for key in sets:
	percentage = (sets[key]['owned_cards'] / sets[key]['total_cards'])
	print("Set: {} | {}/{} ({}%)".format(key, sets[key]['owned_cards'], sets[key]['total_cards'], percentage))
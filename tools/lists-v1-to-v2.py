import json;
import sys;


nouns = [];
adjectives = [];
phrases_s = [];
phrases_p = [];


try:
	with open("nouns.txt", 'r') as file:
		nouns = file.readlines();
		print("loaded nouns. counted {}".format(len(nouns)));
except:
	sys.exit("couldn't load nouns");

try:
	with open("adjectives.txt", 'r') as file:
		adjectives = file.readlines();
		print("loaded adjectives. counted {}".format(len(adjectives)));
except:
	sys.exit("couldn't load adjectives");

try:
	with open("amount.txt", 'r') as file:
		phrases_s = file.readlines();
		print("loaded singular phrases. counted {}".format(len(phrases_s)));
except:
	sys.exit("couldn't load singular phrases");

try:
	with open("amounts.txt", 'r') as file:
		phrases_p = file.readlines();
		print("loaded plural phrases. counted {}".format(len(phrases_p)));
except:
	sys.exit("couldn't load plural phrases");


nouns_out = [];

for noun in nouns:
	noun = noun.strip();

	row = {
		"word": noun.replace("*", ""),
		"can_be_plural": True,
		"proper": False,
		"plural_form": None
	};

	if noun[0] == "*":
		row["can_be_plural"] = False;

	nouns_out.append(row);

try:
	with open("nouns.json", 'w') as file:
		json.dump(nouns_out, file, indent=4, sort_keys=True);
except:
	sys.exit("couldn't write new noun db");


adj_out = [];

for adj in adjectives:
	adj_out.append(adj.strip());

try:
	with open("adjectives.json", 'w') as file:
		json.dump(adj_out, file, indent=4, sort_keys=True);
except:
	sys.exit("couldn't write new adj db");


phrases_s_out = [];

for phrase in phrases_s:
	phrases_s_out.append(phrase.strip());

try:
	with open("phrases_s.json", 'w') as file:
		json.dump(phrases_s_out, file, indent=4, sort_keys=True);
except:
	sys.exit("couldn't write new phrases_s db");


phrases_p_out = [];

for phrase in phrases_p:
	phrases_p_out.append(phrase.strip());

try:
	with open("phrases_p.json", 'w') as file:
		json.dump(phrases_p_out, file, indent=4, sort_keys=True);
except:
	sys.exit("couldn't write new phrases_p db");
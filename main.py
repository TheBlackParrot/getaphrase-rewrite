#!/usr/bin/python

import generator;
import db._db as db;
import random;
import json;

main_choices = [
	"[adjective] [noun]",
	"[article] [adjective] [noun]"
]
template = random.choice(generator.main_choices);
if not random.randint(0, 2):
	template = random.choice(generator.phrases);

test = generator.TemplateString(template);

out = db.add_phrase(str(test));

print(json.dumps(out));
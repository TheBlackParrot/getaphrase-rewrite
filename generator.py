import json;
import sys;
import random;

vowels = ["a", "e", "i", "o", "u"];
nouns = [];
adjectives = [];
phrases_s = [];

try:
	with open('nouns.json', 'r') as file:
		nouns = json.load(file);
except:
	sys.exit("couldn't load nouns!");

try:
	with open('adjectives.json', 'r') as file:
		adjectives = json.load(file);
except:
	sys.exit("couldn't load adjectives!");

# TODO: Merge singular/plural phrases and just make it an argument
try:
	with open('phrases_s.json', 'r') as file:
		phrases_s = json.load(file);
except:
	sys.exit("couldn't load phrases_s!");


proper_nouns = [];
nonproper_nouns = [];
for noun in nouns:
	if noun["proper"]:
		proper_nouns.append(noun);
	else:
		nonproper_nouns.append(noun);


class Noun():
	def __init__(self, args, word=None, can_be_plural=True, proper=False, plural_form=None):
		if not word:
			return;

		self.word = word;
		self.can_be_plural = can_be_plural;
		self.proper = proper;
		self.plural_form = plural_form;

		self.final = word;

		self.args = args;

	def plural(self):
		word = self.word;

		if self.can_be_plural:
			if self.plural_form:
				self.final = self.plural_form;
				return;

			global vowels;

			last_2 = word[-2:];
			last_char = last_2[-1:];

			bypass_check = ["ch", "sh"];
			if last_2 not in bypass_check:
				if last_char == "o" or last_char == "x" or last_char == "s":
					self.final = word + "es";
					return;

				elif last_char == "y":
					if word[-2:-1] in vowels:
						self.final = word + "s";
						return;
					else:
						self.final = word[:-1] + "ies";
						return;

				else:
					self.final = word + "s";
					return;
			else:
				self.final = word + "es";
				return;
		else:
			self.final = word;
			return;

	def __str__(self):
		return self.final;


class Article():
	def __init__(self, args):
		arts = ["a", "the"];
		self.art = random.choice(arts);

		self.args = args;

	def plural(self):
		if "singular" in self.args:
			return;
		self.art = "the";

	def needs_n(self):
		self.art += "n";

	def __str__(self):
		return self.art;


class Adjective():
	def __init__(self, args):
		global adjectives;

		self.parts = set();
		if not random.randint(0, 2):
			self.parts.add(random.choice(adjectives));

		self.parts.add(random.choice(adjectives));

		self.args = args;

	def __str__(self):
		return " ".join(str(part) for part in self.parts);



class TemplateString():
	def __init__(self, data):
		self.raw = data;
		
		self.raw_parts = data.split(" ");
		self.parts = [];

		self.plural_phrase = False;

		global nouns;
		global proper_nouns;
		global nonproper_nouns;
		global vowels;

		for raw_part in self.raw_parts:
			if raw_part[0] == "[" and raw_part[-1:] == "]":
				part_data = raw_part[1:-1];

				args = part_data.split(":");

				if args[0] == "noun":
					if "proper" in args:
						noun = random.choice(proper_nouns);
					elif "nonproper" in args:
						noun = random.choice(nonproper_nouns);
					else:
						noun = random.choice(nouns);

					self.parts.append(Noun(args, **noun));

				elif args[0] == "article":
					self.parts.append(Article(args));

				elif args[0] == "adjective":
					self.parts.append(str(Adjective(args)));
			else:
				self.parts.append(raw_part);

		for index, part in enumerate(self.parts):
			if type(part) == Article:
				if index < len(self.parts):
					next = self.parts[index+1];

					if type(next) == Noun:
						if next.proper:
							self.parts.remove(part);
							continue;

						next = next.word;

					if next[0] in vowels and str(part) in vowels:
						part.needs_n();

			if type(part) == Noun:
				if part.can_be_plural:
					if "singular" not in part.args:
						if not random.randint(0, 2) or "plural" in part.args:
							self.plural_phrase = True;
							part.plural();

		if self.plural_phrase:
			self.phrase_is_plural();


	def phrase_is_plural(self):
		for part in self.parts:
			if type(part) == Article:
				part.plural();


	def __str__(self):
		final = [];

		for part in self.parts:
				final.append(str(part));

		return " ".join(final);

for i in range(0, 20):
	main_choices = [
		"[adjective] [noun]",
		"[article] [adjective] [noun]"
	]
	template = random.choice(main_choices);
	if not random.randint(0, 3):
		template = random.choice(phrases_s);

	test = TemplateString(template);
	print(str(test));
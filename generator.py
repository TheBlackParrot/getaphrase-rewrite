import json;
import sys;
import random;
import re;
import copy;

vowels = ["a", "e", "i", "o", "u"];
nouns = [];
adjectives = [];
phrases = [];
verbs = [];
adverbs = [];

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

try:
	with open('phrases.json', 'r') as file:
		phrases = json.load(file);
except:
	sys.exit("couldn't load phrases!");

try:
	with open('verbs.json', 'r') as file:
		verbs = json.load(file);
except:
	sys.exit("couldn't load verbs!");

try:
	with open('adverbs.json', 'r') as file:
		adverbs = json.load(file);
except:
	sys.exit("couldn't load adverbs!");


proper_nouns = [];
nonproper_nouns = [];
for noun in nouns:
	if "proper" in noun:
		if noun["proper"]:
			proper_nouns.append(noun);
		else:
			nonproper_nouns.append(noun);
	else:
		nonproper_nouns.append(noun);


class Noun():
	def __init__(self, args, word=None, can_be_plural=True, proper=False, plural_form=None, only_plural=False):
		if not word:
			return;

		self.word = word;
		self.can_be_plural = can_be_plural;
		self.proper = proper;
		self.plural_form = plural_form;
		self.only_plural = only_plural;

		self.final = word;

		self.args = args;

	def plural(self):
		word = self.word;

		if self.can_be_plural:
			if self.plural_form:
				self.final = self.plural_form;
				return;

			if self.only_plural:
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


class Verb():
	def __init__(self, args, word=None, past_tense=None, ing=None):
		global verbs;

		self.args = args;


		self.word = word;
		self.past_tense = past_tense;
		self.ing = ing;

		self.final = self.word;

	def to_ing(self):
		self.final = self.ing;

	def to_future_tense(self):
		self.final = " ".join(["will", self.word]);

	def to_past_tense(self):
		self.final = self.past_tense;

	def __str__(self):
		return self.final;


class Adverb():
	def __init__(self, args):
		global adverbs;

		self.args = args;

		self.word = random.choice(adverbs);

	def __str__(self):
		return self.word;


class AfterStr():
	def __init__(self, data):
		self.data = data;

	def __str__(self):
		return self.data;


#reg_safe_part = re.compile(r'[^0-9a-zA-Z\]\:\[]+');
reg_safe_part = re.compile(r'\].*');
class TemplateString():
	def __init__(self, data):
		self.raw = data;
		
		self.raw_parts = data.split(" ");
		self.parts = [];

		self.plural_phrase = False;

		global nouns;
		global proper_nouns;
		global nonproper_nouns;
		global verbs;
		global vowels;
		global reg_safe_part;

		for raw_part in self.raw_parts:
			safe_part = reg_safe_part.sub('', raw_part) + "]";
			after = raw_part.replace(safe_part, "");

			if safe_part[0] == "[" and safe_part[-1:] == "]":
				part_data = safe_part[1:-1];

				args = part_data.split(":");
				if after:
					args.append(AfterStr(after));

				if "again" in args:
					multiple = False;

					if args[0].title() in globals():
						for part in list(reversed(self.parts)):
							if type(part) == globals()[args[0].title()]:
								self.parts.append(copy.deepcopy(part));
								if after:
									self.parts[len(self.parts)-1].args.append(AfterStr(after));
								multiple = True;
								break;

					if multiple:
						continue;

				if args[0] == "noun":
					if "proper" in args:
						noun = random.choice(proper_nouns);
					elif "nonproper" in args:
						noun = random.choice(nonproper_nouns);
					else:
						noun = random.choice(nouns);

					if noun:
						self.parts.append(Noun(args, **noun));

				elif args[0] == "article":
					self.parts.append(Article(args));

				elif args[0] == "adjective":
					self.parts.append(str(Adjective(args)));

				elif args[0] == "verb":
					self.parts.append(Verb(args, **random.choice(verbs)));

				elif args[0] == "adverb":
					self.parts.append(Adverb(args));

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

					try:
						next = next.word;
					except:
						pass;

					if next[0] in vowels and str(part) in vowels:
						part.needs_n();

			if type(part) == Noun:
				if part.can_be_plural:
					if "singular" not in part.args:
						if not random.randint(0, 3) or "plural" in part.args:
							while not part.can_be_plural:
								_ = part.args
								part = Noun(_, **random.choice(nouns));								
							self.plural_phrase = True;
							part.plural();
					elif "singular" in part.args:
						while part.only_plural:
							_ = part.args
							part = Noun(_, **random.choice(nouns));
				else:
					while "plural" in part.args and not part.can_be_plural:
						_ = part.args
						part = Noun(_, **random.choice(nouns));

				if self.parts[index] != part:
					self.parts[index] = part;

			if type(part) == Verb:
				if "ing" in part.args:
					part.to_ing();
				elif "past" in part.args:
					part.to_past_tense();
				elif "future" in part.args:
					part.to_future_tense();


		if self.plural_phrase:
			self.phrase_is_plural();


	def phrase_is_plural(self):
		for part in self.parts:
			if type(part) == Article:
				part.plural();


	def __str__(self):
		final = [];

		for part in self.parts:
			if hasattr(part, 'args'):
				if type(part.args[len(part.args)-1]) == AfterStr:
					final.append(str(part) + str(part.args[len(part.args)-1]));
					continue;

			final.append(str(part));

		return " ".join(final);

main_choices = [
	"[adjective] [noun]",
	"[article] [adjective] [noun]"
]

'''
for i in range(0, 10):
	main_choices = [
		"[adjective] [noun]",
		"[article] [adjective] [noun]"
	]
	template = random.choice(main_choices);
	if not random.randint(0, 2):
		template = random.choice(phrases);

	test = TemplateString(template);
	print(str(test));
'''
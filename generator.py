import json;
import sys;
import random;

vowels = ["a", "e", "i", "o", "u"];
nouns = [];


try:
	with open('nouns.json', 'r') as file:
		nouns = json.load(file);
except:
	sys.exit("couldn't load nouns!");



class Noun():
	def __init__(self, word=None, can_be_plural=True, proper=False, plural_form=None):
		if not word:
			return;

		self.word = word;
		self.can_be_plural = can_be_plural;
		self.proper = proper;
		self.plural_form = plural_form;

	def plural(self):
		word = self.word;

		if self.can_be_plural:
			if self.plural_form:
				return self.plural_form;

			global vowels;

			last_2 = word[-2:];
			last_char = last_2[-1:];

			bypass_check = ["ch", "sh"];
			if last_2 not in bypass_check:
				if last_char == "o" or last_char == "x" or last_char == "s":
					return word + "es";

				elif last_char == "y":
					if word[-2:-1] in vowels:
						return word + "s";
					else:
						return word[:-1] + "ies";

				else:
					return word + "s";
			else:
				return word + "es";
		else:
			return word;

	def __str__(self):
		# for now
		return self.word;


class Article():
	def __init__(self):
		arts = ["a"];
		self.art = random.choice(arts);

	def needs_n(self):
		self.art += "n";

	def __str__(self):
		return self.art;



class TemplateString():
	def __init__(self, data):
		self.raw = data;
		
		self.raw_parts = data.split(" ");
		self.parts = [];

		global nouns;
		global vowels;

		for raw_part in self.raw_parts:
			if raw_part[0] == "[" and raw_part[-1:] == "]":
				part_data = raw_part[1:-1];

				args = part_data.split(" ");

				if args[0] == "noun":
					noun = random.choice(nouns)
					self.parts.append(Noun(**noun));

				elif args[0] == "article":
					self.parts.append(Article());
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


	def __str__(self):
		final = [];

		for part in self.parts:
			if type(part) == Noun:
				final.append(part.word);
			elif type(part) == Article:
				final.append(str(part));
			else:
				final.append(part);

		return " ".join(final);

'''
word = {
	"word": "ox"
}
test = Noun(**word);
print(test.plural());
'''

for i in range(0, 20):
	test = TemplateString("this is [article] [noun]");
	print(str(test));
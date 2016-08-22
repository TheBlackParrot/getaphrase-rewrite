vowels = ["a", "e", "i", "o", "u"];

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



class TemplateString():
	def __init__(self, data):
		self.raw = data;
		
		self.raw_parts = data.split(" ");
		self.parts = [];

		for raw_part in self.raw_parts:
			if raw_part[0] == "[" and raw_part[-1:] == "]":
				part_data = raw_part[1:-1];

				args = part_data.split(" ");

				if args[0] == "noun":
					word = {
						"word": "cake"
					}
					self.parts.append(Noun(**word));
			else:
				self.parts.append(raw_part);

	def __str__(self):
		final = [];

		for part in self.parts:
			if type(part) == Noun:
				final.append(part.word);
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

test = TemplateString("this is a [noun]");
print(str(test));
import generator;
import db._db as db;
import random;

main_choices = [
	"[adjective] [noun]",
	"[article] [adjective] [noun]"
]
template = random.choice(generator.main_choices);
if not random.randint(0, 2):
	template = random.choice(generator.phrases);

test = generator.TemplateString(template);
db.add_phrase(str(test));
print(str(test));

got = db.fetch_phrase(0)
print(got);
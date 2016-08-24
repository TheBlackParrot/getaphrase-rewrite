import db.settings as settings;
import oursql;
from gmpy2 import mpz;
import time;

DBconn = oursql.connect(**settings.SQL);
with DBconn.cursor(oursql.DictCursor) as cursor:
	query = 'CREATE TABLE IF NOT EXISTS cache ( id VARCHAR(8) NOT NULL, phrase TEXT NULL, discovered INT(10) DEFAULT 0, PRIMARY KEY(id) )';
	cursor.execute(query, plain_query=True);

	cursor.close();

def add_phrase(phrase):
	global DBconn;

	with DBconn.cursor(oursql.DictCursor) as cursor:
		query = 'SELECT COUNT(*) FROM cache';
		cursor.execute(query);
		count = cursor.fetchone()["COUNT(*)"];

		query = 'SELECT * FROM cache WHERE phrase = ?';
		cursor.execute(query, [phrase]);

		row = cursor.fetchone();

		if not row:
			query = 'INSERT INTO cache ( id, phrase, discovered ) VALUES ( ?, ?, ? )';
			cursor.execute(query, [mpz(count).digits(32), phrase, time.time()]);
			return {
				"id": mpz(count).digits(32),
				"phrase": phrase,
				"discovered": time.time()
			};

		else:
			return row;

		cursor.close();

def fetch_phrase(idn):
	global DBconn;

	with DBconn.cursor(oursql.DictCursor) as cursor:
		query = 'SELECT * FROM cache WHERE id = ?';
		cursor.execute(query, [idn]);

		row = cursor.fetchone();

		if not row:
			return None;
		else:
			return row;

		cursor.close();
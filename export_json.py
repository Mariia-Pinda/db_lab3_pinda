import json
import psycopg2

username = 'pinda_maria'
password = '111'
database = 'pinda_maria_lab2_DB'

tables = [
    'genres_new',
    'songs_new',
    'artists_new',
    'releases_new',
    'performances_new',
]

conn = psycopg2.connect(user=username, password=password, dbname=database)

data = {}
with conn:
    cur = conn.cursor()

    for table in tables:
        cur.execute('SELECT * FROM ' + table)
        rows = []
        fields = [x[0] for x in cur.description]
        for row in cur:
            rows.append(dict(zip(fields, row)))
        data[table] = rows
with open('all_data.json', 'w') as outf:
    json.dump(data, outf, default=str)
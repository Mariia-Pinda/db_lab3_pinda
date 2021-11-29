import csv
import psycopg2

username = 'pinda_maria'
password = '111'
database = 'pinda_maria_lab2_DB'

output_file_t = 'pinda_DB_{}.csv'

TABLES = [
    'genres_new',
    'songs_new',
    'artists_new',
    'releases_new',
    'performances_new',
]

conn = psycopg2.connect(user=username, password=password, dbname=database)

with conn:
    cur = conn.cursor()

    for table_name in TABLES:
        cur.execute('SELECT * FROM ' + table_name)
        fields = [x[0] for x in cur.description]
        with open(output_file_t.format(table_name), 'w') as outfile:
            writer = csv.writer(outfile)
            writer.writerow(fields)
            for row in cur:
                writer.writerow([str(x) for x in row])
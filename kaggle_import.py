import csv
import psycopg2

username = 'pinda_maria'
password = '111'
database = 'pinda_maria_lab2_DB'

input_csv_file = 'top10s.csv'

query_01 = '''
CREATE TABLE genres_new
(
  genre_id      char(10)  NOT NULL ,
  genre_name    char(50)  NOT NULL ,
  CONSTRAINT pk_genres_new PRIMARY KEY (genre_id)
);
'''

query_02 = '''
CREATE TABLE songs_new
(
  song_id      char(10)  NOT NULL ,
  song_name    char(200)  NOT NULL ,
  CONSTRAINT pk_songs_new PRIMARY KEY (song_id)
);
'''

query_03 = '''
CREATE TABLE artists_new
(
  artist_id      char(10)  NOT NULL ,
  artist_name    char(50)  NOT NULL ,
  CONSTRAINT pk_artists_new PRIMARY KEY (artist_id)
);
'''

query_04 = '''
CREATE TABLE releases_new
(
  release_id      char(10)  NOT NULL ,
  genre_id        char(10)  NOT NULL REFERENCES genres_new(genre_id),
  song_id         char(10)  NOT NULL REFERENCES songs_new(song_id),
  release_date    int       NOT NULL ,
  release_time    time      NULL     ,
  release_place   char(50)  NULL     ,
  CONSTRAINT pk_releases_new PRIMARY KEY (release_id),
  CHECK (release_date >= 2010 and release_date <= 2019)
);
'''

query_05 = '''
CREATE TABLE performances_new
(
  perf_id        char(10)   NOT NULL ,
  artist_id      char(10)   NOT NULL REFERENCES artists_new(artist_id),
  song_id        char(10)   NOT NULL REFERENCES songs_new(song_id),
  perf_date      int        NOT NULL ,
  perf_time      time       NULL     ,
  perf_place     char(50)   NULL     ,
  CONSTRAINT pk_performances_new PRIMARY KEY (perf_id),
  CHECK (perf_date >= 2010 and perf_date <= 2021)
);
'''

query_unique_genre = '''
alter table genres_new add constraint genre_name_constraint unique (genre_name)
'''
query_unique_artist = '''
alter table artists_new add constraint artist_name_constraint unique (artist_name)
'''

query_11 = '''
delete from genres_new
'''
query_12 = '''
delete from songs_new
'''
query_13 = '''
delete from artists_new
'''
query_14 = '''
delete from releases_new
'''
query_15 = '''
delete from performances_new
'''

query_21 = '''
insert into genres_new(genre_id, genre_name) values (%s, %s) ON CONFLICT (genre_name) DO NOTHING
'''
query_22 = '''
insert into songs_new(song_id, song_name) values (%s, %s)
'''
query_23 = '''
insert into artists_new(artist_id, artist_name) values (%s, %s) ON CONFLICT (artist_name) DO NOTHING
'''
query_24 = '''
insert into releases_new(release_id, genre_id, song_id, release_date) values (%s, %s, %s, %s)
'''
query_25 = '''
insert into performances_new(perf_id, artist_id, song_id, perf_date) values (%s, %s, %s, %s)
'''

query_find_genre = '''
select genre_id from genres_new where genre_name = row['top genre']
'''
query_find_artist = '''
select artist_id from artist_new where artist_name = row['artist']
'''

conn = psycopg2.connect(user=username, password=password, dbname=database)

with conn:
    cur = conn.cursor()
    cur.execute(query_15)
    cur.execute(query_14)
    cur.execute(query_13)
    cur.execute(query_12)
    cur.execute(query_11)

    # cur.execute(query_unique_genre)
    # cur.execute(query_unique_artist)

    dict_genres = {}
    dict_artists = {}
    with open(input_csv_file, 'r') as inf:
        reader = csv.DictReader(inf)
        for idx, row in enumerate(reader):
            values1 = (200 + idx, row['top genre'])
            cur.execute(query_21, values1)
            dict_genres[200 + idx] = row['top genre']
            values2 = (1 + idx, row['title'])
            cur.execute(query_22, values2)
            values3 = (31000 + idx, row['artist'])
            cur.execute(query_23, values3)
            dict_artists[31000 + idx] = row['artist']
            values4 = (
            4000 + idx, list(dict_genres.keys())[list(dict_genres.values()).index(row['top genre'])], 1 + idx,
            row['year'])
            cur.execute(query_24, values4)
            values5 = (9500 + idx, list(dict_artists.keys())[list(dict_artists.values()).index(row['artist'])], 1 + idx,
                       row['year'])
            cur.execute(query_25, values5)
    conn.commit()

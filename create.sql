CREATE TABLE genres_new
(
  genre_id      char(10)  NOT NULL ,
  genre_name    char(50)  NOT NULL ,
  CONSTRAINT pk_genres_new PRIMARY KEY (genre_id)
);

CREATE TABLE songs_new
(
  song_id      char(10)  NOT NULL ,
  song_name    char(200)  NOT NULL ,
  CONSTRAINT pk_songs_new PRIMARY KEY (song_id)
);

CREATE TABLE artists_new
(
  artist_id      char(10)  NOT NULL ,
  artist_name    char(50)  NOT NULL ,
  CONSTRAINT pk_artists_new PRIMARY KEY (artist_id)
);

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
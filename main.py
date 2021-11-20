import psycopg2
import matplotlib.pyplot as plt

username = 'pinda_maria'
password = '111'
database = 'pinda_maria_lab2_DB'
host = 'localhost'
port = '5432'

query_1 = '''
create view QuantityGenre as
select trim(genre_name) as genre, count(genre_id) from releases join genres using(genre_id) group by genre_name;
'''

query_2 = '''
create view ArtistCountSongs as
select trim(artist_name) as artist, count(song_id) from artists join performances using(artist_id) group by artist_name;	
'''

query_3 = '''
create view QuantityGenreNotInUSA as
select trim(genre_name) as genre, count(*) from performances join songs using(song_id) join releases using(song_id) 
join genres using(genre_id) where perf_place != 'USA' group by genre_name;
'''

conn = psycopg2.connect(user=username, password=password, dbname=database, host=host, port=port)

with conn:
    cur = conn.cursor()

    cur.execute('drop view if exists QuantityGenre')

    cur.execute(query_1)
    cur.execute('select * from QuantityGenre')
    genres = []
    quantity = []

    print("Query 1")
    for row in cur:
        print(row)
        genres.append(row[0])
        quantity.append(row[1])

    x_range = range(len(genres))

    figure, (bar_ax, pie_ax, graph_ax) = plt.subplots(1, 3)
    plt.subplots_adjust(wspace=0.5)
    bar = bar_ax.bar(x_range, quantity)
    bar_ax.set_title('Кількість пісень кожного жанру')
    bar_ax.set_xlabel('Жанри')
    bar_ax.set_ylabel('Кількість пісень')
    bar_ax.set_xticks(x_range)
    bar_ax.set_xticklabels(genres, fontsize=7)
    for label in bar_ax.get_xticklabels():
        label.set_rotation(30)
        label.set_ha('right')

    cur.execute('drop view if exists ArtistCountSongs')

    cur.execute(query_2)
    cur.execute('select * from ArtistCountSongs')
    artists = []
    songs = []

    print("Query 2")
    for row in cur:
        print(row)
        artists.append(row[0])
        songs.append(row[1])

    pie_ax.pie(songs, labels=artists, autopct='%1.1f%%')
    pie_ax.set_title('Частка пісень, які виконав кожний артист')

    cur.execute('drop view if exists QuantityGenreNotInUSA')

    cur.execute(query_3)
    cur.execute('select * from QuantityGenreNotInUSA')
    place = []
    q_songs = []

    print("Query 3")
    for row in cur:
        print(row)
        place.append(row[0])
        q_songs.append(row[1])

    graph_ax.plot(place, q_songs, marker='o')

    graph_ax.set_xlabel('Жанри')
    graph_ax.set_ylabel('Кількість пісень')
    graph_ax.set_title('Графік залежності кількості пісень, \n що лунають за межами США, від жанру')

    for pl, sng in zip(place, q_songs):
        graph_ax.annotate(sng, xy=(pl, sng), xytext=(2, 3), textcoords='offset points')

mng = plt.get_current_fig_manager()
mng.resize(1400, 750)

plt.show()
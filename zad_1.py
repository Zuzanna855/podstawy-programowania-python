import sqlite3
conn = sqlite3.connect('movies.db')
cursor = conn.cursor()

cursor.execute("CREATE TABLE IF NOT EXISTS movies(movieID, title, genres)")
cursor.execute("CREATE TABLE IF NOT EXISTS links(movieId, imdbId, tmdbId)")
cursor.execute("CREATE TABLE IF NOT EXISTS ratings(userId,movieId,rating,timestamp)")
cursor.execute("CREATE TABLE IF NOT EXISTS tags(userId,movieId,tag,timestamp)")

import pandas as pd
movies = pd.read_csv('C:/Users/PC_Zuzia/Documents/moviesDB/movies.csv')
links  = pd.read_csv('C:/Users/PC_Zuzia/Documents/moviesDB/links.csv')
ratings = pd.read_csv('C:/Users/PC_Zuzia/Documents/moviesDB/ratings.csv')
tags = pd.read_csv('C:/Users/PC_Zuzia/Documents/moviesDB/tags.csv')

movies.to_sql('movies', conn, if_exists='replace', index=False)
links.to_sql('links', conn, if_exists='replace', index=False)
ratings.to_sql('ratings', conn, if_exists='replace', index=False)
tags.to_sql('tags', conn, if_exists='replace', index=False)

cursor.execute("SELECT * FROM movies")
rows = cursor.fetchall()
for row in rows:
    print(row[0], row[1], row[2])

cursor.execute("SELECT * FROM links")
rows = cursor.fetchall()
for row in rows:
    print(row[0], row[1], row[2])

cursor.execute("SELECT * FROM ratings")
rows = cursor.fetchall()
for row in rows:
    print(row[0], row[1], row[2], row[3])

cursor.execute("SELECT * FROM tags")
rows = cursor.fetchall()
for row in rows:
    print(row[0], row[1], row[2], row[3])
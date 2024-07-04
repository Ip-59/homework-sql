DROP TABLE IF EXISTS TrackComp;
DROP TABLE IF EXISTS Compilations;
DROP TABLE IF EXISTS Tracks;
DROP TABLE IF EXISTS ArtAlb;
DROP TABLE IF EXISTS albums;
DROP TABLE IF EXISTS genart;
DROP TABLE IF EXISTS artists;
DROP TABLE IF EXISTS genres;

CREATE TABLE IF NOT EXISTS Genres (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) UNIQUE NOT NULL
);

CREATE TABLE IF NOT EXISTS Artists (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) UNIQUE NOT NULL
);

CREATE TABLE IF NOT EXISTS GenArt (
    genres_id INTEGER NOT NULL REFERENCES Genres (id),
    artists_id INTEGER NOT NULL REFERENCES Artists (id),
    CONSTRAINT pk_GenArt PRIMARY KEY (genres_id, artists_id)
);

CREATE TABLE IF NOT EXISTS Albums (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255) UNIQUE NOT NULL,
    release_year INTEGER CHECK (release_year >= 1900 AND release_year <= extract(year from current_date))
);

CREATE TABLE IF NOT EXISTS ArtAlb (
    artists_id INTEGER NOT NULL REFERENCES Artists (id),
    albums_id INTEGER NOT NULL REFERENCES Albums (id),
    CONSTRAINT pk_ArtAlb PRIMARY KEY (artists_id, albums_id)
);

/* Самый длинный трек из когда-либо записанных в истории длится 13 часов 23 минуты и 32 секунды!
   Композиция под названием The Rise and Fall of Bossanova был создан Майклом и Келли Боствик.
   Они выпустили его 1 ноября 2016 года под псевдонимом P C III, который является одним из
   музыкальных проектов Майкла Боствика.*/

CREATE TABLE IF NOT EXISTS Tracks (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255) UNIQUE NOT NULL,
    duration INTEGER NOT NULL CHECK (duration <= 50000), -- Продолжительность трека в секундах
    albums_id INTEGER NOT NULL REFERENCES Albums (id)
);

CREATE TABLE IF NOT EXISTS Compilations (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255) UNIQUE NOT NULL,
    release_year INTEGER CHECK (release_year >= 1900 AND release_year <= extract(year from current_date))
);

CREATE TABLE IF NOT EXISTS TrackComp (
    tracks_id INTEGER NOT NULL REFERENCES Tracks (id),
    compilations_id INTEGER NOT NULL REFERENCES Compilations (id),
    CONSTRAINT pk_TrackComp PRIMARY KEY (tracks_id, compilations_id)
);

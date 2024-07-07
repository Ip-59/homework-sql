INSERT INTO genres
(id, "name")
VALUES(1, 'Genre 1'),
VALUES(2, 'Genre 2'),
VALUES(3, 'Genre 3');

INSERT INTO artists
(id, "name")
VALUES(1, 'Artist 1'),
VALUES(2, 'Artist-2'),
VALUES(3, 'Artist 3'),
VALUES(4, 'Artist4');

INSERT INTO genart
(genres_id, artists_id)
VALUES(1, 1),
VALUES(2, 2),
VALUES(3, 3),
VALUES(1, 4);

INSERT INTO albums
(id, title, release_year)
VALUES(1, 'Album 1', 2018),
VALUES(2, 'Album 2', 2019),
VALUES(3, 'Album 3', 2020);

INSERT INTO artalb
(artists_id, albums_id)
VALUES(1, 1),
VALUES(2, 2),
VALUES(3, 3),
VALUES(4, 1);

INSERT INTO tracks
(id, title, duration, albums_id)
VALUES(1, 'Track 1', 150, 1),
VALUES(2, 'my Track 2', 180, 2),
VALUES(3, 'Track 3', 210, 3),
VALUES(4, 'my Track 4', 240, 1),
VALUES(5, 'Track 5', 270, 2),
VALUES(6, 'мой Track 6', 300, 3);

INSERT INTO compilations
(id, title, release_year)
VALUES(1, 'Compilation 1', 2021),
VALUES(2, 'Compilation 2', 2020),
VALUES(3, 'Compilation 3', 2019),
VALUES(4, 'Compilation 4', 2018);

INSERT INTO trackcomp
(tracks_id, compilations_id)
VALUES(1, 1),
VALUES(2, 2),
VALUES(3, 3),
VALUES(4, 4),
VALUES(5, 1),
VALUES(6, 2);
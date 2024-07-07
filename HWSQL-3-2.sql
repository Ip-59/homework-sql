SELECT title, duration FROM tracks
WHERE duration = (SELECT MAX(duration) FROM tracks);

SELECT title, duration FROM tracks
WHERE duration >= 210;

SELECT title FROM compilations
WHERE release_year BETWEEN 2018 AND 2020;

SELECT "name" FROM artists
WHERE "name" NOT LIKE '% %';

SELECT title FROM tracks
WHERE title LIKE '%my%' OR title LIKE '%мой%';
SELECT count(artists_id) FROM Genart
GROUP BY genres_id;

SELECT count(*) FROM Tracks t
JOIN Albums al ON al.id = t.albums_id
where release_year = 2019 OR release_year = 2020;

SELECT al.title, avg(t.duratiON) FROM Albums al
JOIN Tracks t ON al.id = t.albums_id 
GROUP BY al.title;

SELECT ar.name FROM Artists ar
JOIN Artalb aa ON ar.id = artists_id
JOIN Albums al ON aa.albums_id = al.id
WHERE al.release_year <> 2020;

SELECT c.title FROM Compilations c
JOIN Trackcomp tc ON tc.compilatiONs_id = c.id
JOIN Tracks t ON t.id = tc.tracks_id
JOIN Albums al ON al.id = t.albums_id
JOIN Artalb aa ON aa.albums_id = al.id
JOIN Artists ar ON ar.id = aa.artists_id
WHERE ar."name" = 'Artist-2';
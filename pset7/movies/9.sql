SELECT people.name FROM stars
JOIN movies ON movies.id = stars.movie_id
JOIN people ON people.id = stars.person_id
WHERE movies.year = 2004
GROUP BY people.id
ORDER BY birth;

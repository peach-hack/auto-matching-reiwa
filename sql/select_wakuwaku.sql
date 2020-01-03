USE auto_matching;

SELECT 
    title,
    name,
    age,
    posted_at,
    genre,
    prefecture,
    city,
    id,
    url
FROM
    posts
WHERE
    site = 'ワクワクメール'
ORDER BY posted_at DESC
LIMIT 10000;

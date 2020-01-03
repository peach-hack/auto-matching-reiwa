USE auto_matching;

SELECT 
    title,
    name,
    age,
    posted_at,
    site,
    genre,
    prefecture,
    city,
    id,
    created_at,
    updated_at
FROM
    posts
ORDER BY posted_at DESC
LIMIT 10000
;

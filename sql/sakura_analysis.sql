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
WHERE
    NOT EXISTS( SELECT 
            word
        FROM
            ng_words
        WHERE
            title LIKE CONCAT('%', word, '%'))
ORDER BY posted_at DESC
LIMIT 10000
;

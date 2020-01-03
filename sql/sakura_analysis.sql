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
    LENGTH(title) < 64
    AND LENGTH(name) < 20
        AND NOT EXISTS( SELECT 
            word
        FROM
            ng_words
        WHERE
            title LIKE CONCAT('%', word, '%'))
        AND name NOT LIKE '%女装%'
        AND name NOT LIKE '%NH%'
        AND name NOT LIKE '%◎%'
        AND name NOT LIKE '%★%'
        AND name NOT LIKE '%☆%'
        AND age NOT LIKE '%40%'
        AND age NOT LIKE '%50%'
        AND age NOT LIKE '%60%'
ORDER BY posted_at DESC
LIMIT 10000
;

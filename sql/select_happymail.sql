USE auto_matching;

SELECT 
    title, name, age, post_at, genre, prefecture, city, id, url
FROM
    posts
WHERE
    site = 'ハッピーメール'
LIMIT 10000;

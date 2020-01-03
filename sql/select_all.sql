USE auto_matching;

SELECT 
    title, name, age, posted_at, site, genre, prefecture, city, id, url, image_url, profile_id
FROM
    posts
ORDER BY posted_at DESC
;

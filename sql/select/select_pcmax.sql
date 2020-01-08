-- USE auto_matching;
SELECT
  title,
  name,
  age,
  posted_at,
  genre,
  prefecture,
  city,
  id,
  profile_id,
  url,
  profile_url
FROM posts
WHERE
  site = 'PCMAX'
ORDER BY
  posted_at DESC
LIMIT
  10000;
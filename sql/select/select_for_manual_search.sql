-- USE auto_matching;
SELECT
  posted_at,
  title,
  name,
  age,
  site,
  genre,
  prefecture,
  city,
  url,
  profile_url
FROM posts
ORDER BY
  posted_at DESC
LIMIT
  10000;
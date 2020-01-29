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
  id,
  url,
  created_at,
  updated_at,
  image_url,
  profile_id,
  profile_url
FROM posts
WHERE
  posted_at < NOW()
ORDER BY
  posted_at DESC
LIMIT
  10000;
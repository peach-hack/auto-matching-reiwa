-- USE auto_matching;
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
  url,
  created_at,
  updated_at,
  image_url,
  profile_id
FROM posts
ORDER BY
  posted_at DESC
LIMIT
  1000;
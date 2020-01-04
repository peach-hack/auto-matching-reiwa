-- お泊まりサーチ
SELECT
  posted_at,
  title,
  name,
  age,
  site,
  genre,
  prefecture,
  city,
  url
FROM posts
WHERE
  title LIKE '%泊%'
ORDER BY
  posted_at DESC
LIMIT
  30;
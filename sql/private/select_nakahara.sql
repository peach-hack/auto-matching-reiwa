-- 徒歩で会えそうな近所の人サーチ
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
  city LIKE '%中原区%'
  OR title LIKE '%小杉%'
ORDER BY
  posted_at DESC;
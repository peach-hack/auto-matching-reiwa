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
  url,
  profile_url
FROM posts
WHERE
  city LIKE '%中原区%'
  OR title LIKE '%小杉%'
  OR city LIKE '%高津区%'
ORDER BY
  posted_at DESC;
WITH title_freqs AS (
  SELECT
    title as title_f,
    COUNT(title) as title_count
  FROM posts
  WHERE
    site = 'メルパラ'
    OR site = 'ミントJメール'
  GROUP BY
    title_f
)
SELECT
  posted_at,
  site,
  title,
  name,
  age,
  genre,
  prefecture,
  city,
  title_count,
  id,
  url
FROM posts as p
LEFT JOIN title_freqs ON title_f = p.title
WHERE
  (
    site = 'メルパラ'
    OR site = 'ミントJメール'
  ) --
  --
  AND title_count = 1
ORDER BY
  posted_at DESC;
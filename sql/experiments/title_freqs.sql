SELECT
  title as title,
  COUNT(title) as title_count
FROM posts
GROUP BY
  title
ORDER BY
  title_count DESC;
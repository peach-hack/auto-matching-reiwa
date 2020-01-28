SELECT
  COUNT(id)
  posted_at
FROM posts
WHERE posted_at > (NOW() - INTERVAL 3 DAY);
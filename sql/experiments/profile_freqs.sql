SELECT
  CONCAT(name, '_', age, '_', city) as profile,
  COUNT(CONCAT(name, '_', age, '_', city)) as profile_count
FROM posts
GROUP BY
  profile
ORDER BY
  profile_count DESC
  ;
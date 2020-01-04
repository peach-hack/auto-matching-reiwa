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
  created_at,
  updated_at,
  id
FROM posts as p
WHERE
  LENGTH(title) < 64
  AND LENGTH(name) < 20 -- AND NOT EXISTS(
  --   SELECT
  --     word
  --   FROM ng_words as ng
  --   WHERE
  --     title LIKE CONCAT('%', ng.word, '%')
  -- )
  AND NOT EXISTS(
    SELECT
      name
    FROM ng_names
    WHERE
      p.name LIKE CONCAT('%', name, '%')
  )
  -- AND NOT EXISTS(
  --   SELECT
  --     age
  --   FROM ng_ages
  --   WHERE
  --     age LIKE CONCAT('%', age, '%')
  -- )
ORDER BY
  posted_at DESC
LIMIT
  10000;
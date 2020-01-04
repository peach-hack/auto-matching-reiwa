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
  -- タイトルが長すぎる投稿は除外
  LENGTH(title) < 64 -- 名前が長すぎる投稿は除外
  AND LENGTH(name) < 20 -- 年齢が対象外の人は除外
  AND NOT EXISTS(
    SELECT
      age
    FROM ng_ages
    WHERE
      p.age LIKE CONCAT(age, '%')
  ) -- 名前にNGワードが含まれている投稿を除外
  AND NOT EXISTS(
    SELECT
      name
    FROM ng_names
    WHERE
      p.name LIKE CONCAT('%', name, '%')
  ) -- タイトルにNGワードが含まれている投稿を除外
  AND NOT EXISTS(
    SELECT
      word
    FROM ng_words as ng
    WHERE
      p.title LIKE CONCAT('%', word, '%')
  ) -- 投稿日時順に並べ替え
ORDER BY
  posted_at DESC
LIMIT
  3000;
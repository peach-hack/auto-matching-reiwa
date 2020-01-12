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
  url
FROM posts
WHERE
  genre LIKE '大人のﾒｰﾙ/TEL'
  OR genre LIKE 'Hなお話'
  OR genre LIKE 'エロトーク・TELH'
  OR genre LIKE 'メールH'
ORDER BY
  posted_at DESC
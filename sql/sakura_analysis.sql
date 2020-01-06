--
-- サクラ判定
--
WITH title_freqs AS (
  SELECT
    title as title_f,
    COUNT(title) as title_count
  FROM posts
  GROUP BY
    title_f
),
profile_freqs AS (
  SELECT
    CONCAT(name, '_', age, '_', city) as profile,
    COUNT(CONCAT(name, '_', age, '_', city)) as profile_count
  FROM posts
  GROUP BY
    profile
)
SELECT
  posted_at,
  title,
  name,
  age,
  site,
  genre,
  prefecture,
  city,
  title_count,
  profile_count,
  created_at,
  updated_at,
  url
FROM posts as p
LEFT JOIN title_freqs ON title_f = p.title
LEFT JOIN profile_freqs ON profile = CONCAT(name, '_', age, '_', city)
WHERE
  -- ジャンルによるフィルタ
  -- ハッピーメールでピュアのレコードが混じってしまう
  genre != '大人のﾒｰﾙ/TEL'
  AND genre != '恋人募集'
  AND genre != 'メル友募集'
  AND genre != '全国ﾒﾙ友'
  AND genre != '友達募集'
  AND genre != '今からあそぼ'
  AND genre != '既婚者'
  AND genre != '既婚者希望'
  AND genre != '画像掲示板'
  AND genre != '全国アダルト'
  AND genre != 'ミドルエイジアダルト'
  AND genre != 'ミドルエイジ'
  AND genre != 'ﾐﾄﾞﾙｴｲｼﾞ/ｼﾆｱ' --
  --
  -- タイトルが長すぎる投稿は除外
  AND LENGTH(p.title) < 48 --
  --
  -- 名前が長すぎる投稿は除外
  AND LENGTH(name) < 24 --
  --
  -- 地域による除外は保留。
  -- 地方から都会に来て募集してる場合がある。
  --
  -- 年齢が対象外の人は除外
  AND NOT EXISTS(
    SELECT
      age
    FROM ng_ages
    WHERE
      p.age LIKE CONCAT(age, '%')
  ) --
  --
  -- 名前にNGワードが含まれている投稿を除外
  AND NOT EXISTS(
    SELECT
      name
    FROM ng_names
    WHERE
      p.name LIKE CONCAT('%', name, '%')
  ) --
  --
  -- タイトルにNGワードが含まれている投稿を除外
  AND NOT EXISTS(
    SELECT
      word
    FROM ng_words as ng
    WHERE
      p.title LIKE CONCAT('%', word, '%')
  ) --
  --
  -- タイトルとプロフィールの出現回数の制限
  AND profile_count <= 2
  AND title_count = 1 --
  --
  -- created_atとupdated_atの乖離があるものは再投稿を繰り替えしているので除外
  AND (updated_at - INTERVAL 6 HOUR) < created_at --
  --
  --
  -- 1日以内を列挙
  -- AND posted_at > (NOW() - INTERVAL 1 DAY)
  --
  -- 3時間以内を列挙
  AND posted_at > (NOW() - INTERVAL 3 HOUR)
ORDER BY
  posted_at DESC;
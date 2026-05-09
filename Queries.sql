-- 1. Total number of games
SELECT
  COUNT(*) AS total_games
FROM `final-project-495422.game_analytics.cleaned_games`;

-- 2. Number of games by genre
SELECT
  genre_primary,
  COUNT(*) AS game_count
FROM `final-project-495422.game_analytics.cleaned_games`
GROUP BY genre_primary
ORDER BY game_count DESC;

-- 3. Number of games by publisher
SELECT
  publisher,
  COUNT(*) AS game_count
FROM `final-project-495422.game_analytics.cleaned_games`
WHERE publisher != 'Unknown'
  AND total_reviews >= 30
GROUP BY publisher
ORDER BY game_count DESC
LIMIT 20;

-- 4. Free-to-play vs paid games
SELECT
  game_type,
  COUNT(*) AS game_count,
  SUM(positive_reviews) AS total_positive_reviews,
  SUM(negative_reviews) AS total_negative_reviews,
  SUM(total_reviews) AS total_reviews,
  ROUND(SAFE_DIVIDE(SUM(positive_reviews), SUM(total_reviews)) * 100, 2) AS weighted_positive_review_percent,
FROM `final-project-495422.game_analytics.cleaned_games`
WHERE total_reviews >= 30
GROUP BY game_type;

-- 5. Price distribution
SELECT
  CASE
    WHEN price_final = 0 THEN 'Free'
    WHEN price_final > 0 AND price_final <= 5 THEN '$0.01 - $5'
    WHEN price_final > 5 AND price_final <= 10 THEN '$5.01 - $10'
    WHEN price_final > 10 AND price_final <= 20 THEN '$10.01 - $20'
    WHEN price_final > 20 AND price_final <= 40 THEN '$20.01 - $40'
    ELSE 'Over $40'
  END AS price_range,
  COUNT(*) AS game_count
FROM `final-project-495422.game_analytics.cleaned_games`
GROUP BY price_range
ORDER BY game_count DESC;

-- 6. Top games by peak concurrent users
SELECT
  name,
  genre_primary,
  publisher,
  peak_ccu
FROM `final-project-495422.game_analytics.cleaned_games`
WHERE peak_ccu > 0
ORDER BY peak_ccu DESC
LIMIT 20;

-- 7. Average peak CCU by genre
SELECT
  genre_primary,
  COUNT(*) AS game_count,
  ROUND(AVG(peak_ccu), 2) AS avg_peak_ccu
FROM `final-project-495422.game_analytics.cleaned_games`
WHERE peak_ccu > 0
  AND total_reviews >= 30
GROUP BY genre_primary
ORDER BY avg_peak_ccu DESC
LIMIT 20;

-- 8. Review pattern by genre
SELECT
  genre_primary,
  COUNT(*) AS game_count,
  SUM(positive_reviews) AS total_positive_reviews,
  SUM(negative_reviews) AS total_negative_reviews,
  SUM(total_reviews) AS total_reviews,
  ROUND(SAFE_DIVIDE(SUM(positive_reviews), SUM(total_reviews)) * 100, 2) AS weighted_positive_review_percent
FROM `final-project-495422.game_analytics.cleaned_games`
WHERE total_reviews >= 30
GROUP BY genre_primary
ORDER BY weighted_positive_review_percent DESC
LIMIT 20;
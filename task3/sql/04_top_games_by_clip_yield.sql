-- metric 4: top games by volume & yield
-- yield = clips per session. game mana yg paling produktif generate clip -
-- buat prioritasin model quality & marketing partnership.
SELECT
    g.game_name,
    count(distinct g.id) as sessions,
    count(c.id) as clips,
    round(1.0 * count(c.id) / count(distinct g.id), 1) as clips_per_session
FROM gamesession g
JOIN clips c ON c.gamesession_Id = g.id
GROUP BY g.game_name
ORDER BY clips DESC
LIMIT 10;
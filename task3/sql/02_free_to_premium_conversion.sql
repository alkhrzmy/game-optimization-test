-- metric 2: free -> premium conversion
-- active user = pernah submit minimal 1 gamesession. hitung berapa persen
-- yg convert ke premium. rate rendah = value prop lemah atau upgrade funnel bocor.
SELECT
    count(distinct g.user_id) as active_users,
    count(distinct p.user_id) as converted,
    round(100.0 * count(distinct p.user_id) / count(distinct g.user_id), 2) as conv_rate
FROM gamesession g
LEFT JOIN premium p ON p.user_id = g.user_id;
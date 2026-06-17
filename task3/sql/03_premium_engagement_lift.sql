-- metric 3: premium engagement lift
-- bikin clip per user segment. kalo premium bikin lebih byk dari free,
-- berarti premium tier emang dipake user yg heavy - value prop valid.
WITH user_clips AS (
    SELECT user_id, count(*) as clips_made
    FROM clips
    GROUP BY user_id
)
SELECT
    CASE WHEN p.user_id IS NOT NULL THEN 'Premium' ELSE 'Free' END as segment,
    count(distinct uc.user_id) as users,
    sum(uc.clips_made) as total_clips,
    round(avg(uc.clips_made), 1) as avg_clips
FROM user_clips uc
LEFT JOIN premium p ON p.user_id = uc.user_id
GROUP BY segment
ORDER BY avg_clips DESC;
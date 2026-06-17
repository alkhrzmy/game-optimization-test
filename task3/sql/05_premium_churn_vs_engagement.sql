-- metric 5: premium churn vs engagement
-- churned user rata-rata bikin clip lebih dikit dari retained? kalo iya,
-- low early engagement bisa jadi early warning sign sebelum cancel.
WITH prem AS (
    SELECT user_id,
           max(case when canceled_at is not null then 1 else 0 end) as ever_canceled
    FROM premium
    GROUP BY user_id
),
user_clips AS (
    SELECT user_id, count(*) as clips_made
    FROM clips
    GROUP BY user_id
)
SELECT
    CASE WHEN pr.ever_canceled = 1 THEN 'Churned' ELSE 'Retained' END as status,
    count(distinct pr.user_id) as users,
    round(avg(coalesce(uc.clips_made, 0)), 1) as avg_clips
FROM prem pr
LEFT JOIN user_clips uc ON uc.user_id = pr.user_id
GROUP BY status
ORDER BY status;
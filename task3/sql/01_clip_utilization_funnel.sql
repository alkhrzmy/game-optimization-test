-- clip funnel: generated -> downloaded -> shared
-- nge-check apakah output AI beneran dipake user. clip yg generate
-- tapi ga pernah di-download/shared = zero value buat product.
SELECT
    count(distinct c.id) as generated,
    count(distinct d.clip_id) as downloaded,
    count(distinct s.clip_id) as shared,
    round(100.0 * count(distinct d.clip_id) / count(distinct c.id), 2) as dl_rate,
    round(100.0 * count(distinct s.clip_id) / count(distinct c.id), 2) as share_rate
from clips c
left join downloaded_clips d on d.clip_id = c.id
left join shared_clips s on s.clip_id = c.id;

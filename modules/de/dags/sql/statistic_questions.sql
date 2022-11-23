select t1.store_idx,EXTRACT(YEAR FROM date) as "year", EXTRACT(MONTH FROM date) as "month", AVG(t1.value), COUNT(t1.value) from sales t1
left join stores t2
on t1.idx = t2.idx
group by (t1.store_idx, "month", "year")
order by t1.store_idx, "year", "month"

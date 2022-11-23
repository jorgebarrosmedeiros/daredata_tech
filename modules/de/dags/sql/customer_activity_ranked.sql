create table customer_activity_ranked
as 
select idx,
       valid_from,
	   valid_to,
	   scd_a,
	   scd_b,
       RANK() OVER(PARTITION BY idx ORDER BY valid_from DESC) activity_rank
FROM customer_activity
INSERT INTO cdm.dm_settlement_report (
    restaurant_id,
    restaurant_name,
    settlement_date,
    orders_count,
    orders_total_sum,
    orders_bonus_payment_sum,
    orders_bonus_granted_sum,
    order_processing_fee,
    restaurant_reward_sum
)
SELECT
    dr.id, 
    dr.restaurant_name,
    dt.ts::date,
    count(distinct do2.id) as orders_count, 
    SUM(total_sum) AS orders_total_sum,
    SUM(bonus_payment) AS orders_bonus_payment_sum,
    SUM(bonus_grant) AS orders_bonus_granted_sum,
    SUM(total_sum) * 0.25 AS order_processing_fee,
    SUM(total_sum) * 0.75 - sum (bonus_payment) AS restaurant_reward_sum
from dds.fct_product_sales ps
join dds.dm_products dp on ps.product_id = dp.id
join dds.dm_restaurants dr on dp.restaurant_id = dr.id 
join dds.dm_orders do2 on ps.order_id = do2.id 
join dds.dm_users du on du.id = do2.user_id 
join dds.dm_timestamps dt on dt.id  = do2.timestamp_id 
where do2.order_status like 'CLOSED'
group by dr.id, dr.restaurant_name, dt.ts::date
ON CONFLICT (restaurant_id, settlement_date) DO UPDATE
SET
    orders_count = EXCLUDED.orders_count,
    orders_total_sum = EXCLUDED.orders_total_sum,
    orders_bonus_payment_sum = EXCLUDED.orders_bonus_payment_sum,
    orders_bonus_granted_sum = EXCLUDED.orders_bonus_granted_sum,
    order_processing_fee = EXCLUDED.order_processing_fee,
    restaurant_reward_sum = EXCLUDED.restaurant_reward_sum;

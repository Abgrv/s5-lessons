select 
	current_timestamp as test_date_time, 
	'test_01'         as test_name, 
	count(*) = 0      as test_result
from (
	select * 
	from public_test.dm_settlement_report_expected as ex 
    full join public_test.dm_settlement_report_actual as ac
            on  ex.id                       = ac.id 
            and ex.restaurant_id            = ac.restaurant_id 
            and ex.settlement_year          = ac.settlement_year 
            and ex.settlement_month         = ac.settlement_month 
            and ex.orders_count             = ac.orders_count
            and ex.orders_total_sum         = ac.orders_total_sum
            and ex.orders_bonus_payment_sum = ac.orders_bonus_payment_sum
            and ex.orders_bonus_granted_sum = ac.orders_bonus_granted_sum
            and ex.order_processing_fee     = ac.order_processing_fee
            and ex.restaurant_reward_sum    = ac.restaurant_reward_sum
     where ex.id is null or ac.id is NULL
     ) as T
;
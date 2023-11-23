ALTER TABLE cdm.dm_settlement_report 
ALTER COLUMN orders_count SET DEFAULT 0;
ALTER TABLE cdm.dm_settlement_report 
ALTER COLUMN orders_total_sum SET DEFAULT 0;
ALTER TABLE cdm.dm_settlement_report 
ALTER COLUMN orders_bonus_payment_sum SET DEFAULT 0;
ALTER TABLE cdm.dm_settlement_report 
ALTER COLUMN orders_bonus_granted_sum SET DEFAULT 0;
ALTER TABLE cdm.dm_settlement_report 
ALTER COLUMN order_processing_fee SET DEFAULT 0;
ALTER TABLE cdm.dm_settlement_report 
ALTER COLUMN restaurant_reward_sum SET DEFAULT 0;

ALTER TABLE cdm.dm_settlement_report 
ADD CONSTRAINT orders_count_not_null CHECK (orders_count >= 0);
ALTER TABLE cdm.dm_settlement_report 
ADD CONSTRAINT orders_total_sum_not_null CHECK (orders_total_sum >= 0);
ALTER TABLE cdm.dm_settlement_report 
ADD CONSTRAINT orders_bonus_payment_sum_not_null CHECK (orders_bonus_payment_sum >= 0);
ALTER TABLE cdm.dm_settlement_report 
ADD CONSTRAINT orders_bonus_granted_sum_not_null CHECK (orders_bonus_granted_sum >= 0);
ALTER TABLE cdm.dm_settlement_report 
ADD CONSTRAINT order_processing_fee_not_null CHECK (order_processing_fee >= 0);
ALTER TABLE cdm.dm_settlement_report 
ADD CONSTRAINT restaurant_reward_sum_not_null CHECK (restaurant_reward_sum >= 0);

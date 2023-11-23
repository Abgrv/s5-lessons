CREATE TABLE cdm.dm_settlement_report (
    id serial PRIMARY KEY,
    restaurant_id varchar NOT NULL,
    restaurant_name varchar NOT NULL,
    settlement_date date NOT NULL,
    orders_count integer NOT NULL,
    orders_total_sum numeric(14, 2) NOT NULL,
    orders_bonus_payment_sum numeric(14, 2) NOT NULL,
    orders_bonus_granted_sum numeric(14, 2) NOT NULL,
    order_processing_fee numeric(14, 2) NOT NULL,
    restaurant_reward_sum numeric(14, 2) NOT NULL
);

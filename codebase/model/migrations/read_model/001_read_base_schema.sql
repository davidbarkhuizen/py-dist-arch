-- ============================================================================================
-- buy_order

CREATE TABLE buy_order_read_model(

    id INTEGER NOT NULL,
    client_id INTEGER NOT NULL,
    external_id UUID NOT NULL,
    created_at TIMESTAMPTZ NOT NULL,

    currency_id INTEGER NOT NULL,
    currency_iso3 NCHAR(3) NOT NULL,

    currency_amount NUMERIC(12, 2) NOT NULL,
    btc_rate NUMERIC(20, 8) NOT NULL,
    btc_amount NUMERIC(11, 8) NOT NULL
);

CREATE INDEX buy_order_read_created_at_index 
ON buy_order_read_model
(
    created_at DESC
);

CREATE INDEX buy_order_read_model_page_index_alpha
ON buy_order_read_model
(
    client_id,
    external_id
);

CREATE INDEX buy_order_read_model_page_index_beta
ON buy_order_read_model
(
    client_id,
    id,
    created_at DESC
);
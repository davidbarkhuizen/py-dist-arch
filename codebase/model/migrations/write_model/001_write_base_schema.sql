CREATE EXTENSION pgcrypto;

-- ============================================================================================

CREATE TABLE client (

    id INTEGER GENERATED ALWAYS AS IDENTITY,
        PRIMARY KEY(id),
    
    email VARCHAR(254) NOT NULL UNIQUE
);

-- ============================================================================================

CREATE TABLE currency (

    id INTEGER GENERATED ALWAYS AS IDENTITY,
        PRIMARY KEY(id),

    iso3 NCHAR(3) NOT NULL UNIQUE,

    dp SMALLINT NOT NULL
        CHECK ((dp > 0) AND (dp <= 2))
);

-- ============================================================================================

CREATE TABLE buy_order_running_total (

    btc_amount NUMERIC(12, 8)
        CHECK (btc_amount <= 100.0)
);


INSERT INTO buy_order_running_total(btc_amount) VALUES (0);

-- on delete

CREATE OR REPLACE FUNCTION buy_order_running_total_delete_trigger_fn()
    RETURNS trigger AS
    $$
        BEGIN
            RAISE EXCEPTION 'cannot delete record from buy_order_running_total'; 
        END;
    $$
LANGUAGE 'plpgsql';

CREATE TRIGGER buy_order_running_total_delete_trigger
BEFORE DELETE
ON "buy_order_running_total"
FOR EACH ROW
EXECUTE PROCEDURE buy_order_running_total_delete_trigger_fn();

-- on insert

CREATE OR REPLACE FUNCTION buy_order_running_total_insert_trigger_fn()
    RETURNS trigger AS
    $$
        BEGIN
            IF ((SELECT COUNT(*) FROM "buy_order_running_total") > 0) THEN
                RAISE EXCEPTION 'buy_order_running_total can have at most one record'; 
            END IF;
        END;
    $$
LANGUAGE 'plpgsql';

CREATE TRIGGER buy_order_insert_trigger
AFTER INSERT
ON "buy_order_running_total"
FOR EACH ROW
EXECUTE PROCEDURE buy_order_running_total_insert_trigger_fn();

-- ============================================================================================

CREATE TABLE buy_order (

    id INTEGER GENERATED ALWAYS AS IDENTITY,
        PRIMARY KEY(id),

    created_at TIMESTAMPTZ NOT NULL
        DEFAULT now(),

    external_id UUID NOT NULL
         DEFAULT GEN_RANDOM_UUID(),

    client_id INTEGER NOT NULL,
    CONSTRAINT fk_client_id
        FOREIGN KEY(client_id) 
	    REFERENCES client(id),

    currency_id INTEGER NOT NULL,
    CONSTRAINT fk_currency
        FOREIGN KEY(currency_id) 
	    REFERENCES currency(id),
    
    currency_amount NUMERIC(12, 2) NOT NULL
        check (currency_amount <= 1000000000),
    
    -- 1 000 000 000 000.00 00 00 00 (trillion) USD : 1 BTC
    btc_rate NUMERIC(20, 8) NOT NULL,

    btc_amount NUMERIC(11, 8) NOT NULL
        CHECK (0 < btc_amount)
);

-- on delete

CREATE OR REPLACE FUNCTION buy_order_delete_trigger_fn()
    RETURNS trigger AS
    $$
        BEGIN
            RAISE EXCEPTION 'cannot delete record from buy_order'; 
        END;
    $$
LANGUAGE 'plpgsql';

CREATE TRIGGER buy_order_delete_trigger
BEFORE DELETE
ON "buy_order"
FOR EACH ROW
EXECUTE PROCEDURE buy_order_delete_trigger_fn();

-- on update

CREATE OR REPLACE FUNCTION buy_order_update_trigger_fn()
    RETURNS trigger AS
    $$
        BEGIN
            RAISE EXCEPTION 'cannot update record in buy_order'; 
        END;
    $$
LANGUAGE 'plpgsql';

CREATE TRIGGER buy_order_update_trigger
BEFORE UPDATE
ON "buy_order"
FOR EACH ROW
EXECUTE PROCEDURE buy_order_update_trigger_fn();

-- ============================================================================================

CREATE OR REPLACE FUNCTION buy_order_insert_trigger_fn()
  RETURNS trigger AS
$$
    BEGIN

        UPDATE buy_order_running_total
        SET btc_amount = btc_amount + NEW."btc_amount";
        
        RETURN NEW;
    END;
$$

LANGUAGE 'plpgsql';

CREATE TRIGGER buy_order_insert_trigger
AFTER INSERT
ON "buy_order"
FOR EACH ROW
EXECUTE PROCEDURE buy_order_insert_trigger_fn();

-- ============================================================================================

CREATE TABLE buy_order_idempotence_cache (

    client_id INTEGER NOT NULL,
    currency_id INT NOT NULL,
    currency_amount NUMERIC(12, 2) NOT NULL,
    idempotence_key UUID NOT NULL,

    PRIMARY KEY (client_id, currency_id, currency_amount, idempotence_key),

    created_at TIMESTAMPTZ NOT NULL
        DEFAULT now(),

    buy_order_id INTEGER NOT NULL
);
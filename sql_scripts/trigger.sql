CREATE OR REPLACE FUNCTION notify_seller_sell()
    RETURNS TRIGGER
    LANGUAGE PLPGSQL
AS
$$
DECLARE
    id_seller integer;
BEGIN

    select distinct seller_customer_id_user 
        from quantity as q, product as pr 
       where q.product_id_prod = pr.id_prod and pr.id_prod = NEW.product_id_prod 
    INTO id_seller;

    INSERT INTO notifications
        (message, date, was_read, customer_id_user)
        VALUES
        ('A product was sold!', current_date, false, id_seller);
    return NEW;

END;
$$;

DROP TRIGGER IF EXISTS notify_seller_sell_trigger ON quantity;

CREATE TRIGGER notify_seller_sell_trigger 
    AFTER INSERT
    ON "quantity"
    FOR EACH ROW
EXECUTE PROCEDURE notify_seller_sell();

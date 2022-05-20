
-- notification of product selled
CREATE OR REPLACE FUNCTION notify_seller_sell()
    RETURNS TRIGGER
    LANGUAGE PLPGSQL
AS
$$
DECLARE
    id_seller integer;
    id_prod   integer;
BEGIN

    select distinct seller_customer_id_user 
        from quantity as q, product as pr 
       where q.product_id_prod = pr.id_prod and pr.id_prod = NEW.product_id_prod 
    INTO id_seller;
    
    select distinct pr.id_prod 
        from quantity as q, product as pr 
       where q.product_id_prod = pr.id_prod and pr.id_prod = NEW.product_id_prod 
    INTO id_prod;
    

    INSERT INTO notifications
        (message, date, was_read, customer_id_user)
        VALUES
        (FORMAT('The product: %s was sold!', id_prod), current_date, false, id_seller);
    return NEW;

END;
$$;

DROP TRIGGER IF EXISTS notify_seller_sell_trigger ON quantity;

CREATE TRIGGER notify_seller_sell_trigger 
    AFTER INSERT
    ON "quantity"
    FOR EACH ROW
EXECUTE PROCEDURE notify_seller_sell();



-- notification of questions
CREATE OR REPLACE FUNCTION notify_seller_question()
    RETURNS TRIGGER
    LANGUAGE PLPGSQL
AS
$$
DECLARE
    id_seller integer;
    id_prod   integer;
BEGIN

    SELECT DISTINCT pdt.seller_customer_id_user
        FROM forum as f INNER JOIN product as pdt
            ON f.product_id_prod = pdt.id_prod
        WHERE f.forum_id_forum IS NULL AND f.id_forum = NEW.id_forum
    INTO id_seller;
    
    SELECT DISTINCT pdt.id_prod
        FROM forum as f INNER JOIN product as pdt
            ON f.product_id_prod = pdt.id_prod
        WHERE f.forum_id_forum IS NULL AND f.id_forum = NEW.id_forum
    INTO id_prod;


    IF id_seller IS NOT NULL THEN

        INSERT INTO notifications
            (message, date, was_read, customer_id_user)
            VALUES
            ( FORMAT('Someone made a question in your product: %s!', id_prod), current_date, false, id_seller);

    END IF;
    return NEW;
END;
$$;

DROP TRIGGER IF EXISTS notify_seller_question_trigger ON forum;

CREATE TRIGGER notify_seller_question_trigger 
    AFTER INSERT
    ON "forum"
    FOR EACH ROW
EXECUTE PROCEDURE notify_seller_question();



-- notification to user who receive a comment
CREATE OR REPLACE FUNCTION notify_user_answer()
    RETURNS TRIGGER
    LANGUAGE PLPGSQL
AS
$$
DECLARE
    id_user integer;

BEGIN
    SELECT customer_id_user FROM forum WHERE id_forum =
        (SELECT forum_id_forum
            FROM forum
            where id_forum = NEW.id_forum AND forum_id_forum IS NOT null)
    INTO id_user;



    IF id_user IS NOT NULL THEN
        INSERT INTO notifications
            (message, date, was_read, customer_id_user)
        VALUES
            ('Someone answered your question/comment', current_date, false, id_user);
    END IF;
    
    return NEW;

END;
$$;

DROP TRIGGER IF EXISTS notify_user_answer_trigger ON forum;

CREATE TRIGGER notify_user_answer_trigger
    AFTER INSERT
    ON "forum"
    FOR EACH ROW
EXECUTE PROCEDURE notify_user_answer();

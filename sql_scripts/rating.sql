CREATE OR REPLACE PROCEDURE GiveRating (
    Id_Cust NUMERIC,
    Id_Prod NUMERIC,
    Rating  NUMERIC,
    Comment VARCHAR(512)
)
LANGUAGE 'plpgsql'
AS $$

    DECLARE 
        CountOrders int;
        CountRating int;

BEGIN 

    SELECT CountOrders = count(*) FROM customer WHERE customer.id_user IN 
        (SELECT to_order.buyer_customer_id_user 
           FROM quantity INNER JOIN to_order 
             ON quantity.to_order_id_order = to_order.id_order 
          WHERE product_id_prod = Id_Prod AND to_order.buyer_customer_id_user = Id_Cust
        );


    SELECT CountRating = count(id_rating)
      FROM rating 
     WHERE buyer_customer_id_user = Id_Cust and product_id_prod = Id_Prod;

    
    IF CountOrders > 0 AND CountRating = 0
        THEN
            INSERT INTO rating (rating, comment, buyer_customer_id_user, product_id_prod) 
                 VALUES (Rating, Comment, Id_Cust, Id_Prod);
            
    END IF;
END;
$$;

CALL GiveRating(31, 4, 4, 'Muito Bom');
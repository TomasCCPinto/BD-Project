-- alterar o nome do user, order e admin

CREATE TABLE product (
	id_prod		 		BIGINT,
	description	 		VARCHAR(512) NOT NULL,
	stock		 		BIGINT NOT NULL,
	price		 		FLOAT(8) NOT NULL,
	seller_user_id_user BIGINT NOT NULL,

	PRIMARY KEY(id_prod)
);

CREATE TABLE features (
	type		 	VARCHAR(512) NOT NULL,
	type_value	 	INTEGER NOT NULL,
	product_id_prod BIGINT NOT NULL
);

CREATE TABLE seller (
	user_id_user BIGINT,

	PRIMARY KEY(user_id_user)
);

CREATE TABLE customer (
	bought		     BOOL NOT NULL,
	rating_id_rating BIGINT,
	user_id_user	 BIGINT,

	PRIMARY KEY(user_id_user)
);

CREATE TABLE order_sell (
	id_order		 	  BIGINT,
	customer_user_id_user BIGINT NOT NULL,

	PRIMARY KEY(id_order)
);

CREATE TABLE rating (
	id_rating	 	BIGINT,
	rating		 	INTEGER NOT NULL,
	comment	 	 	VARCHAR(512) NOT NULL,
	product_id_prod BIGINT NOT NULL,

	PRIMARY KEY(id_rating)
);

CREATE TABLE history (
	id_hist	 	 	BIGINT NOT NULL,
	description	 	VARCHAR(512) NOT NULL,
	stock		 	BIGINT NOT NULL,
	price		 	FLOAT(8) NOT NULL,
	his_date	 	DATE NOT NULL,
	product_id_prod BIGINT NOT NULL
);

CREATE TABLE user_table (
	id_user  BIGINT,
	name	 VARCHAR(512) NOT NULL,
	nif	 	 BIGINT NOT NULL,
	adress	 VARCHAR(512) NOT NULL,

	PRIMARY KEY(id_user)
);

CREATE TABLE admin_table (
	user_id_user BIGINT,

	PRIMARY KEY(user_id_user)
);

CREATE TABLE forum_notifications (
	if_forum			 	 	 BIGINT,
	comment			 	 	 	 VARCHAR(512) NOT NULL,
	notifications_id		 	 BIGINT UNIQUE NOT NULL,
	notifications_message	 	 VARCHAR(512) NOT NULL,
	notifications_time_stamp	 TIMESTAMP NOT NULL,
	notifications_was_read	 	 BOOL NOT NULL,
	user_id_user		 	 	 BIGINT NOT NULL,
	order_id_order		 	 	 BIGINT NOT NULL,
	forum_notifications_if_forum BIGINT,
	product_id_prod		 		 BIGINT NOT NULL,

	PRIMARY KEY(if_forum)
);

CREATE TABLE campaign (
	id		 		   BIGINT,
	data_begin	 	   DATE NOT NULL,
	data_end		   DATE NOT NULL,
	n_coupon		   INTEGER NOT NULL,
	n_coupon_used	   INTEGER NOT NULL,
	discount		   INTEGER NOT NULL,
	expiration_days	   INTEGER NOT NULL,
	admin_user_id_user BIGINT NOT NULL,

	PRIMARY KEY(id)
);

CREATE TABLE coupon (
	id			 	 	  BIGINT,
	purchase_date	 	  BOOL NOT NULL,
	customer_user_id_user BIGINT NOT NULL,
	campaign_id		 	  BIGINT NOT NULL,

	PRIMARY KEY(id)
);

CREATE TABLE quantity (
	quantity	 	INTEGER NOT NULL,
	order_id_order	BIGINT,
	product_id_prod BIGINT,

	PRIMARY KEY(order_id_order,product_id_prod)
);

CREATE TABLE customer_campaign (
	customer_user_id_user BIGINT,
	campaign_id		 	  BIGINT,

	PRIMARY KEY(customer_user_id_user,campaign_id)
);

ALTER TABLE product  	  		  ADD CONSTRAINT product_fk1  	 		 FOREIGN KEY (seller_user_id_user) 	 		REFERENCES seller(user_id_user);
ALTER TABLE features 	  		  ADD CONSTRAINT features_fk1 	 		 FOREIGN KEY (product_id_prod)     	 		REFERENCES product(id_prod);
ALTER TABLE seller   	  		  ADD CONSTRAINT seller_fk1   	 		 FOREIGN KEY (user_id_user)        	 		REFERENCES user_table(id_user);
ALTER TABLE customer 	  		  ADD CONSTRAINT customer_fk1 	 		 FOREIGN KEY (rating_id_rating)    	 		REFERENCES rating(id_rating);
ALTER TABLE customer 	  		  ADD CONSTRAINT customer_fk2 	 		 FOREIGN KEY (user_id_user) 	   	 		REFERENCES user_table(id_user);
ALTER TABLE order_sell    	  	  ADD CONSTRAINT order_fk1    	 		 FOREIGN KEY (customer_user_id_user) 		REFERENCES customer(user_id_user);
ALTER TABLE rating   	  		  ADD CONSTRAINT rating_fk1   	 		 FOREIGN KEY (product_id_prod) 		 		REFERENCES product(id_prod);
ALTER TABLE history  	  		  ADD CONSTRAINT history_fk1  	 		 FOREIGN KEY (product_id_prod) 		 		REFERENCES product(id_prod);
ALTER TABLE admin_table 		  ADD CONSTRAINT admin_table_fk1 		 FOREIGN KEY (user_id_user)    		 		REFERENCES user_table(id_user);
ALTER TABLE forum_notifications   ADD CONSTRAINT forum_notifications_fk1 FOREIGN KEY (user_id_user)    		 		REFERENCES user_table(id_user);
ALTER TABLE forum_notifications   ADD CONSTRAINT forum_notifications_fk2 FOREIGN KEY (order_id_order)  		 		REFERENCES order_sell(id_order);
ALTER TABLE forum_notifications   ADD CONSTRAINT forum_notifications_fk3 FOREIGN KEY (forum_notifications_if_forum) REFERENCES forum_notifications(if_forum);
ALTER TABLE forum_notifications   ADD CONSTRAINT forum_notifications_fk4 FOREIGN KEY (product_id_prod) 	     		REFERENCES product(id_prod);
ALTER TABLE campaign 			  ADD CONSTRAINT campaign_fk1 		     FOREIGN KEY (admin_user_id_user)    		REFERENCES admin_table(user_id_user);
ALTER TABLE coupon   			  ADD CONSTRAINT coupon_fk1   		     FOREIGN KEY (customer_user_id_user) 		REFERENCES customer(user_id_user);
ALTER TABLE coupon   			  ADD CONSTRAINT coupon_fk2   		     FOREIGN KEY (campaign_id)     		 		REFERENCES campaign(id);
ALTER TABLE quantity 			  ADD CONSTRAINT quantity_fk1 		     FOREIGN KEY (order_id_order)  		 		REFERENCES order_sell(id_order);
ALTER TABLE quantity 			  ADD CONSTRAINT quantity_fk2 		     FOREIGN KEY (product_id_prod) 		 		REFERENCES product(id_prod);
ALTER TABLE customer_campaign     ADD CONSTRAINT customer_campaign_fk1   FOREIGN KEY (customer_user_id_user) 		REFERENCES customer(user_id_user);
ALTER TABLE customer_campaign     ADD CONSTRAINT customer_campaign_fk2   FOREIGN KEY (campaign_id) 					REFERENCES campaign(id);
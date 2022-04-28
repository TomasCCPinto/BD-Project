CREATE TABLE product (
	id_prod		 	BIGSERIAL,
	name			VARCHAR(50) NOT NULL,
	description		 VARCHAR(512) NOT NULL,
	stock			 BIGINT NOT NULL,
	price			 FLOAT(8) NOT NULL,
	seller_customer_id_user BIGINT NOT NULL,
	PRIMARY KEY(id_prod)
);

CREATE TABLE features (
	type		 VARCHAR(512) NOT NULL,
	type_value	 INTEGER NOT NULL,
	product_id_prod BIGINT NOT NULL
);

CREATE TABLE seller (
	customer_id_user BIGINT,
	PRIMARY KEY(customer_id_user)
);

CREATE TABLE buyer (
	customer_id_user BIGINT,
	PRIMARY KEY(customer_id_user)
);

CREATE TABLE to_order (
	id_order		 BIGINT,
	buyer_customer_id_user BIGINT NOT NULL,
	PRIMARY KEY(id_order)
);

CREATE TABLE rating (
	id_rating		 BIGINT,
	rating		 INTEGER NOT NULL,
	comment		 VARCHAR(512),
	--this pair should be unique
	buyer_customer_id_user BIGINT NOT NULL,
	product_id_prod	 BIGINT NOT NULL,
	PRIMARY KEY(id_rating)
);

CREATE TABLE history (
	id_hist	 BIGINT NOT NULL,
	description	 VARCHAR(512) NOT NULL,
	price		 FLOAT(8) NOT NULL,
	his_date	 DATE,
	product_id_prod BIGINT NOT NULL
);

CREATE TABLE customer (
	id_user	 BIGSERIAL NOT NULL,
	name	 VARCHAR(512) NOT NULL,
	nif	 	 BIGINT NOT NULL,
	adress	 VARCHAR(512) NOT NULL,
	email	 VARCHAR(512) NOT NULL,
	password VARCHAR(512) NOT NULL,

	PRIMARY KEY(id_user)
);

CREATE TABLE administrator (
	customer_id_user BIGINT,
	
	PRIMARY KEY(customer_id_user)
);

CREATE TABLE forum_notifications (
	if_forum			 BIGINT,
	comment			 VARCHAR(512) NOT NULL,
	notifications_id		 BIGINT UNIQUE NOT NULL,
	notifications_message	 VARCHAR(512) NOT NULL,
	notifications_time_stamp	 TIMESTAMP NOT NULL,
	notifications_was_read	 BOOL NOT NULL,
	customer_id_user		 BIGINT NOT NULL,
	to_order_id_order		 BIGINT NOT NULL,
	forum_notifications_if_forum BIGINT,
	product_id_prod		 BIGINT NOT NULL,
	PRIMARY KEY(if_forum)
);

CREATE TABLE campaign (
	id				 BIGINT,
	data_begin			 DATE NOT NULL,
	data_end			 DATE NOT NULL,
	n_coupon			 INTEGER NOT NULL,
	n_coupon_used			 INTEGER NOT NULL,
	discount			 INTEGER NOT NULL,
	expiration_days		 INTEGER NOT NULL,
	administrator_customer_id_user BIGINT NOT NULL,
	PRIMARY KEY(id)
);

CREATE TABLE coupon (
	id			 BIGINT,
	purchase_date		 BOOL NOT NULL,
	buyer_customer_id_user BIGINT NOT NULL,
	campaign_id		 BIGINT NOT NULL,
	PRIMARY KEY(id)
);

CREATE TABLE quantity (
	quantity		 INTEGER NOT NULL,
	to_order_id_order BIGINT,
	product_id_prod	 BIGINT,
	PRIMARY KEY(to_order_id_order,product_id_prod)
);

CREATE TABLE buyer_campaign (
	buyer_customer_id_user BIGINT,
	campaign_id		 BIGINT,
	PRIMARY KEY(buyer_customer_id_user,campaign_id)
);

ALTER TABLE product ADD CONSTRAINT product_fk1 FOREIGN KEY (seller_customer_id_user) REFERENCES seller(customer_id_user);
ALTER TABLE features ADD CONSTRAINT features_fk1 FOREIGN KEY (product_id_prod) REFERENCES product(id_prod);
ALTER TABLE seller ADD CONSTRAINT seller_fk1 FOREIGN KEY (customer_id_user) REFERENCES customer(id_user);
ALTER TABLE buyer ADD CONSTRAINT buyer_fk1 FOREIGN KEY (customer_id_user) REFERENCES customer(id_user);
ALTER TABLE to_order ADD CONSTRAINT to_order_fk1 FOREIGN KEY (buyer_customer_id_user) REFERENCES buyer(customer_id_user);
ALTER TABLE rating ADD CONSTRAINT rating_fk1 FOREIGN KEY (buyer_customer_id_user) REFERENCES buyer(customer_id_user);
ALTER TABLE rating ADD CONSTRAINT rating_fk2 FOREIGN KEY (product_id_prod) REFERENCES product(id_prod);
ALTER TABLE history ADD CONSTRAINT history_fk1 FOREIGN KEY (product_id_prod) REFERENCES product(id_prod);
ALTER TABLE administrator ADD CONSTRAINT administrator_fk1 FOREIGN KEY (customer_id_user) REFERENCES customer(id_user);
ALTER TABLE forum_notifications ADD CONSTRAINT forum_notifications_fk1 FOREIGN KEY (customer_id_user) REFERENCES customer(id_user);
ALTER TABLE forum_notifications ADD CONSTRAINT forum_notifications_fk2 FOREIGN KEY (to_order_id_order) REFERENCES to_order(id_order);
ALTER TABLE forum_notifications ADD CONSTRAINT forum_notifications_fk3 FOREIGN KEY (forum_notifications_if_forum) REFERENCES forum_notifications(if_forum);
ALTER TABLE forum_notifications ADD CONSTRAINT forum_notifications_fk4 FOREIGN KEY (product_id_prod) REFERENCES product(id_prod);
ALTER TABLE campaign ADD CONSTRAINT campaign_fk1 FOREIGN KEY (administrator_customer_id_user) REFERENCES administrator(customer_id_user);
ALTER TABLE coupon ADD CONSTRAINT coupon_fk1 FOREIGN KEY (buyer_customer_id_user) REFERENCES buyer(customer_id_user);
ALTER TABLE coupon ADD CONSTRAINT coupon_fk2 FOREIGN KEY (campaign_id) REFERENCES campaign(id);
ALTER TABLE quantity ADD CONSTRAINT quantity_fk1 FOREIGN KEY (to_order_id_order) REFERENCES to_order(id_order);
ALTER TABLE quantity ADD CONSTRAINT quantity_fk2 FOREIGN KEY (product_id_prod) REFERENCES product(id_prod);
ALTER TABLE buyer_campaign ADD CONSTRAINT buyer_campaign_fk1 FOREIGN KEY (buyer_customer_id_user) REFERENCES buyer(customer_id_user);
ALTER TABLE buyer_campaign ADD CONSTRAINT buyer_campaign_fk2 FOREIGN KEY (campaign_id) REFERENCES campaign(id);

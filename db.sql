--- TODO переделать структуру БД

CREATE SEQUENCE users_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;

ALTER SEQUENCE users_id_seq OWNED BY users.id;



CREATE TABLE users (
    id bigint NOT NULL DEFAULT nextval('users_id_seq'),
    first_name varchar(200), 
    last_name varchar(200),
    user_id int, 
    phone_number int,
    PRIMARY KEY (id)
);


CREATE SEQUENCE expenses_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE expenses_id_seq OWNED BY expenses.id;


CREATE TABLE expenses (
    id bigint NOT NULL DEFAULT nextval('expenses_id_seq'),
    health int,
    education int,
    entertainment int,
    travaling int,
    food int,
    apartment int,
    internet_and_connection int,
    large_purchases int,
    extra_spending int,
    add_time timestamp,
    PRIMARY KEY (id)
);


CREATE SEQUENCE user_expenses_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE user_expenses_id_seq OWNED BY user_expenses.id;


CREATE TABLE user_expenses (
    id bigint NOT NULL DEFAULT nextval('user_expenses_id_seq'),
    user_id bigint NOT NULL,
    expenses_id bigint NOT NULL,
    PRIMARY KEY (id),
    CONSTRAINT fk_expenses_id
      FOREIGN KEY(expenses_id)
	  REFERENCES expenses(id),
    CONSTRAINT fk_expenses_user_id
      FOREIGN KEY(user_id)
	  REFERENCES users(id)
);


CREATE SEQUENCE income_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE income_id_seq OWNED BY income.id;


CREATE TABLE income (
    id bigint NOT NULL DEFAULT nextval('income_id_seq'),
    salary int, 
    part_time_job int, 
    dividends_and_coupons int,
    add_time timestamp,
    PRIMARY KEY (id)
);


CREATE SEQUENCE user_income_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE user_income_id_seq OWNED BY user_income.id;


CREATE TABLE user_income (
    id bigint NOT NULL DEFAULT nextval('user_income_id_seq'),
    user_id bigint NOT NULL,
    income_id bigint NOT NULL,
    PRIMARY KEY (id),
    CONSTRAINT fk_income_id
      FOREIGN KEY(income_id)
	  REFERENCES income(id),
    CONSTRAINT fk_income_user_id
      FOREIGN KEY(user_id)
	  REFERENCES users(id)
);


CREATE SEQUENCE investments_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE investments_id_seq OWNED BY investments.id;


CREATE TABLE investments (
    id bigint NOT NULL DEFAULT nextval('investments_id_seq'),
    invested int, 
    total_amount int,
    add_time timestamp,
    PRIMARY KEY (id)
);


CREATE SEQUENCE user_investments_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE user_investments_id_seq OWNED BY user_investments.id;


CREATE TABLE user_investments (
    id bigint NOT NULL DEFAULT nextval('user_investments_id_seq'),
    user_id bigint NOT NULL,
    investments_id bigint NOT NULL,
    PRIMARY KEY (id),
    CONSTRAINT fk_investments_id
      FOREIGN KEY(investments_id)
	  REFERENCES investments(id),
    CONSTRAINT fk_investments_user_id
      FOREIGN KEY(user_id)
	  REFERENCES users(id)
);
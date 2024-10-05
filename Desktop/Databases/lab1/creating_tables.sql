-- DROP TABLE public."users" CASCADE;

CREATE TABLE IF NOT EXISTS public."users" (

    user_id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    role VARCHAR(20) CHECK (role IN ('tenant', 'landlord')) NOT NULL
);

TABLESPACE pg_default;
ALTER TABLE public."users"
 OWNER to postgres;

--------------------------------
-- DROP TABLE public."rental" CASCADE;

CREATE TABLE IF NOT EXISTS public."rental" (
    rental_id SERIAL PRIMARY KEY,
    user_id INT REFERENCES Users(user_id)  NOT NULL,
    title VARCHAR(50) NOT NULL,
    description VARCHAR(1000) NOT NULL,
    price DECIMAL(12, 2) NOT NULL
);

TABLESPACE pg_default;
ALTER TABLE public."rental"
 OWNER to postgres;


--------------------------------
-- DROP TABLE public."reservation" CASCADE;

CREATE TABLE IF NOT EXISTS public."reservation" (
    reservation_id SERIAL PRIMARY KEY,
    rental_id INT REFERENCES Rental(rental_id)  NOT NULL,
    start_date DATE NOT NULL,
    end_date DATE NOT NULL
);

TABLESPACE pg_default;
ALTER TABLE public."reservation"
 OWNER to postgres;


--------------------------------
-- DROP TABLE public."transactions" CASCADE;

CREATE TABLE IF NOT EXISTS public."transactions" (
    transaction_id SERIAL PRIMARY KEY,
    reservation_id INT REFERENCES Reservation(reservation_id) NOT NULL,
    user_id INT REFERENCES Users(user_id) NOT NULL
);

TABLESPACE pg_default;
ALTER TABLE public."transactions"
 OWNER to postgres;


--------------------------------
-- DROP TABLE public."reviews" CASCADE;

CREATE TABLE IF NOT EXISTS public."reviews" (
    review_id SERIAL PRIMARY KEY,
    user_id INT REFERENCES Users(user_id)  NOT NULL,
	rental_id INT REFERENCES Rental(rental_id)  NOT NULL,
    rating INT CHECK (rating BETWEEN 1 AND 5) NOT NULL,
    comment TEXT
);

TABLESPACE pg_default;
ALTER TABLE public."reviews"
 OWNER to postgres;
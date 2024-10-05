INSERT INTO users (name, email, role)
VALUES 
('Dmytro', 'dmitr@gmail.com', 'landlord'),
('John', 'john@mail.com','tenant');

select * from users


INSERT INTO rental (user_id, title, description, price)
VALUES 
(9, 'квартира', 'Вул. Київська, 12, Київ', 50000),
(9, 'будинок', 'Вул. Гагарина, 5, Житомир', 100000);

select * from rental


INSERT INTO reservation (rental_id, start_date, end_date)
VALUES 
(11, '2024-10-01', '2025-09-30'),
(12, '2024-10-15', '2025-10-14');

select * from reservation

INSERT INTO transactions (reservation_id, user_id)
VALUES 
(5, 10),
(6, 10);

select * from transactions

INSERT INTO reviews (user_id, rental_id, rating, comment)
VALUES 
(10, 11, 5, 'Хороші умови та ціна'),
(10, 12, 4, '');

select * from reviews

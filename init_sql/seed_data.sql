CREATE TABLE IF NOT EXISTS trips (
    id SERIAL PRIMARY KEY,
    rider_name VARCHAR(100),
    start_location VARCHAR(100),
    end_location VARCHAR(100),
    fare DECIMAL(6,2),
    trip_date DATE
);

INSERT INTO trips (rider_name, start_location, end_location, fare, trip_date) VALUES
('Alice', 'Airport', 'Downtown', 23.50, '2025-04-20'),
('Bob', 'University', 'Mall', 15.00, '2025-04-21'),
('Charlie', 'Stadium', 'Museum', 18.25, '2025-04-22');
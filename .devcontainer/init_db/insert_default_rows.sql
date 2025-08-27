-- Insert sample employees
INSERT INTO employee_list (first_name, surname, position, department, phone_number, email, birth_date, status, description, register_time)
VALUES
('John', 'Doe', 0, 0, '010-0000-0001', 'john.doe1@example.com', '1990-01-01', 1, 'Sample employee 1', '2023-01-01 09:00:00'),
('Jane', 'Smith', 1, 1, '010-0000-0002', 'jane.smith2@example.com', '1989-02-02', 1, 'Sample employee 2', '2023-01-02 09:00:00'),
('Alice', 'Johnson', 2, 2, '010-0000-0003', 'alice.johnson3@example.com', '1991-03-03', 1, 'Sample employee 3', '2023-01-03 09:00:00'),
('Bob', 'Williams', 0, 1, '010-0000-0004', 'bob.williams4@example.com', '1992-04-04', 1, 'Sample employee 4', '2023-01-04 09:00:00'),
('Charlie', 'Brown', 1, 0, '010-0000-0005', 'charlie.brown5@example.com', '1993-05-05', 1, 'Sample employee 5', '2023-01-05 09:00:00'),
('David', 'Lee', 2, 1, '010-0000-0006', 'david.lee6@example.com', '1994-06-06', 1, 'Sample employee 6', '2023-01-06 09:00:00'),
('Eve', 'Kim', 0, 2, '010-0000-0007', 'eve.kim7@example.com', '1995-07-07', 1, 'Sample employee 7', '2023-01-07 09:00:00'),
('Frank', 'Park', 1, 2, '010-0000-0008', 'frank.park8@example.com', '1996-08-08', 1, 'Sample employee 8', '2023-01-08 09:00:00'),
('Grace', 'Choi', 2, 0, '010-0000-0009', 'grace.choi9@example.com', '1997-09-09', 1, 'Sample employee 9', '2023-01-09 09:00:00'),
('Hank', 'Jung', 0, 1, '010-0000-0010', 'hank.jung10@example.com', '1998-10-10', 1, 'Sample employee 10', '2023-01-10 09:00:00')

-- Insert sample document approvals
INSERT INTO document_approval (issuer, assignee, status, dayoff_start_date, dayoff_end_date, reason)
VALUES
(1, 2, 0, '2023-05-01', '2023-05-02', 'Vacation'),
(2, 1, 1, '2023-05-03', '2023-05-03', 'Personal'),
(3, 2, 2, '2023-05-04', '2023-05-05', 'Family event'),
(4, 1, 0, '2023-05-06', '2023-05-06', 'Medical'),
(5, 2, 1, '2023-05-07', '2023-05-08', 'Travel'),
(6, 1, 2, '2023-05-09', '2023-05-09', 'Other'),
(7, 3, 0, '2023-05-10', '2023-05-11', 'Vacation'),
(8, 5, 1, '2023-05-12', '2023-05-12', 'Personal'),
(9, 7, 2, '2023-05-13', '2023-05-14', 'Family event'),
(10, 9, 0, '2023-05-15', '2023-05-15', 'Medical')

-- Test SELECT operation
SELECT * FROM User;
SELECT * FROM Amenity;

-- Test INSERT operation
INSERT INTO User (id, first_name, last_name, email, password, is_admin)
VALUES ('123e4567-e89b-12d3-a456-426614174000', 'John', 'Doe', 'john.doe@example.com', '$2b$12$KIXQ1b8Q5Z1e1Q1e1Q1e1e1Q1e1Q1e1Q1e1Q1e1Q1e1Q1e1Q1e1Q', FALSE);

-- Test UPDATE operation
UPDATE User SET first_name = 'Jane' WHERE id = '123e4567-e89b-12d3-a456-426614174000';

-- Test DELETE operation
DELETE FROM User WHERE id = '123e4567-e89b-12d3-a456-426614174000';

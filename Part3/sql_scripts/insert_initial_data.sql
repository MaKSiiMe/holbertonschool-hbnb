-- Insert Administrator User
INSERT INTO User (id, first_name, last_name, email, password, is_admin)
VALUES ('36c9050e-ddd3-4c3b-9731-9f487208bbc1', 'Admin', 'HBnB', 'admin@hbnb.io', '$2b$12$KIXQ1b8Q5Z1e1Q1e1Q1e1e1Q1e1Q1e1Q1e1Q1e1Q1e1Q1e1Q1e1Q', TRUE);

-- Insert Initial Amenities
INSERT INTO Amenity (id, name) VALUES
('a1b2c3d4-e5f6-7g8h-9i0j-k1l2m3n4o5p6', 'WiFi'),
('b2c3d4e5-f6g7-h8i9-j0k1-l2m3n4o5p6q7', 'Swimming Pool'),
('c3d4e5f6-g7h8-i9j0-k1l2-m3n4o5p6q7r8', 'Air Conditioning');

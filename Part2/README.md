# HBnB Project - Part 2

## Overview
This project implements the Business Logic and API endpoints for the HBnB application using Flask and Flask-RESTx. It includes CRUD operations for Users, Places, Reviews, and Amenities.

## Project Structure

hbnb/
├── app/
│ ├── api/
│ │ └── v1/
│ │ ├── users.py
│ │ ├── places.py
│ │ ├── reviews.py
│ │ └── amenities.py
│ ├── models/
│ │ ├── user.py
│ │ ├── place.py
│ │ ├── review.py
│ │ └── amenity.py
│ ├── services/
│ │ └── facade.py
│ └── init.py
├── tests/
│ ├── test_users.py
│ ├── test_places.py
│ ├── test_reviews.py
│ └── test_amenities.py
├── config.py
├── run.py
├── requirements.txt
└── README.md


## Installation
1. Clone the repository.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt

Running the Application
python run.py

Testing
Run tests using pytest:
pytest tests/

API Documentation
Access the Swagger UI at http://localhost:5000/api/v1/.

Endpoints
Users: POST /api/v1/users/, GET /api/v1/users/, etc.

Places: POST /api/v1/places/, GET /api/v1/places/<place_id>, etc.

Reviews: POST /api/v1/reviews/, GET /api/v1/reviews/<review_id>, etc.

Amenities: POST /api/v1/amenities/, GET /api/v1/amenities/<amenity_id>, etc.

Validation Rules
Users: Valid email format, unique email.

Places: Positive price, valid latitude/longitude.

Reviews: Rating between 1-5, valid user and place IDs.

## Troubleshooting
1. **Test Failures**:  
   - Ensure all API requests include required fields (e.g., `owner_id` for places).  
   - Validate email formats (e.g., `user@example.com`).  

2. **Swagger Documentation**:  
   Access `http://localhost:5000/api/v1/` to verify endpoint schemas and test via the UI.

3. **Data Persistence**:  
   The in-memory repository resets on server restart. Use POST requests to repopulate data.
  
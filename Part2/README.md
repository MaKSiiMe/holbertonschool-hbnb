# 🏠 HBnB Project   

## Project Objective: Web Application  - PART 2

## Description

The **HBnB** project is a full-stack web application that simulates a simplified version of Airbnb. This second phase focuses on building a RESTful API with Flask, implementing persistent data storage using SQLAlchemy, and structuring the application for scalability and maintainability.

## Features

- **User Authentication & Management**: Secure user registration, login, and role-based access control.
- **CRUD Operations**: Create, Read, Update, and Delete functionality for Places, Users, Reviews, and Amenities.
- **RESTful API**: Versioned endpoints for seamless integration with frontend or third-party services.
- **Data Persistence**: SQLAlchemy ORM for robust database management.
- **Facade Pattern**: Simplified service layer interactions via `app/services/facade.py`.

## Project Structure

hbnb/
├── app/
│ ├── init.py # Initializes Flask app and dependencies
│ ├── api/
│ │ ├── init.py # API blueprint registration
│ │ ├── v1/ # API version 1 endpoints
│ │ ├── init.py
│ │ ├── users.py # User-related routes
│ │ ├── places.py # Place-related routes
│ │ ├── reviews.py # Review-related routes
│ │ ├── amenities.py # Amenity-related routes
│ ├── models/
│ │ ├── init.py # Model imports and relationships
│ │ ├── user.py # User model definition
│ │ ├── place.py # Place model definition
│ │ ├── review.py # Review model definition
│ │ ├── amenity.py # Amenity model definition
│ ├── services/
│ │ ├── init.py
│ │ ├── facade.py # Facade pattern for service abstraction
│ ├── persistence/
│ ├── init.py
│ ├── repository.py # Database interaction layer
├── run.py # Application entry point
├── config.py # Environment configuration
├── requirements.txt # Project dependencies
├── README.md # Project documentation

Copy

## Core Components

### Models

#### `BaseModel` (Base Class)
- **Attributes**:
  - `id` (UUID4): Unique identifier.
  - `created_at` (DateTime): Creation timestamp.
  - `updated_at` (DateTime): Last update timestamp.
- **Methods**:
  - `save()`: Updates `updated_at` on changes.
  - `update(**kwargs)`: Updates attributes via dictionary.

#### `User` (Inherits `BaseModel`)
- **Attributes**:
  - `first_name`, `last_name` (String, max 50 chars)
  - `email` (String, unique, validated format)
  - `is_admin` (Boolean, default `False`)

#### `Place` (Inherits `BaseModel`)
- **Attributes**:
  - `title` (String, max 100 chars)
  - `description` (String, optional)
  - `price` (Float, must be positive)
  - `latitude`, `longitude` (Float, geolocation)
  - `owner` (Relationship to `User`)
- **Methods**:
  - `add_review()`, `add_amenity()`

#### `Review` (Inherits `BaseModel`)
- **Attributes**:
  - `text` (String, required)
  - `rating` (Integer, 1-5)
  - `place` (Relationship to `Place`)
  - `user` (Relationship to `User`)

#### `Amenity` (Inherits `BaseModel`)
- **Attributes**:
  - `name` (String, max 50 chars)

### 👤 Contributors:  
- [David Tolza](https://github.com/VidadTol)  
- [Giovanni Farias](https://github.com/ginftls)  
- [Ludiane Trouillefou](https://github.com/ludiane-tr)  
- [Maxime Truel](https://github.com/MaKSiiMe)  
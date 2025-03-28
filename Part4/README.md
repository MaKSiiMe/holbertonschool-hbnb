<<<<<<< HEAD
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

```
hbnb/
├── app/
│   ├── __init__.py
│   ├── api/
│   │   ├── __init__.py
│   │   ├── v1/
│   │       ├── __init__.py
│   │       ├── users.py
│   │       ├── places.py
│   │       ├── reviews.py
│   │       ├── amenities.py
│   ├── models/
│   │   ├── __init__.py
│   │   ├── user.py
│   │   ├── place.py
│   │   ├── review.py
│   │   ├── amenity.py
│   ├── services/
│   │   ├── __init__.py
│   │   ├── facade.py
│   ├── persistence/
│       ├── __init__.py
│       ├── repository.py
├── run.py
├── config.py
├── requirements.txt
├── README.md
```

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

#### `Amenity` (Inherits `BaseModel`)
- **Attributes**:
  - `name` (String, max 50 chars)
  
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
=======
# <img src="https://cdn.prod.website-files.com/6105315644a26f77912a1ada/63eea844ae4e3022154e2878_Holberton-p-800.png" width="150" /> - HBNB Project - Cohort C#25  
The HBnB project at Holberton is a simplified full-stack clone of Airbnb. It covers various aspects of software development, including backend, database management, front-end integration, and deployment.

---

### 📘 [Part 1: UML Diagrams](https://github.com/MaKSiiMe/holbertonschool-hbnb/tree/main/Part1)  
We started the development of the HBnB Evolution application by creating a detailed blueprint. This technical documentation compiles essential diagrams and explanations, serving as a comprehensive guide to the system’s architecture, design, and implementation steps, from user interactions to database operations.  

#### Key Points:  
1. [High-level architecture](https://github.com/MaKSiiMe/holbertonschool-hbnb/blob/main/Part1/0-%20High-Level_Package_Diagram.md) with a package diagram outlining the three layers and the use of the **Facade Pattern**.

2. [Detailed diagrams of the business logic layer](https://github.com/MaKSiiMe/holbertonschool-hbnb/blob/main/Part1/1-%20Detailed_Class_Diagram_for_Business_Logic_Layer.md) illustrating key entities, their relationships, and their role in the system.

3. [Sequence diagrams for key API interactions](https://github.com/MaKSiiMe/holbertonschool-hbnb/blob/main/Part1/2-%20Sequence_diagram_for_API_calls.md) depicting critical operations such as:  
    - [User registration](https://github.com/MaKSiiMe/holbertonschool-hbnb/blob/main/Part1/2-%20Sequence_diagram_for_user_registration.md)  
    - [Place creation](https://github.com/MaKSiiMe/holbertonschool-hbnb/blob/main/Part1/2-%20Sequence_diagram_for_place_creation.md)  
    - [Review submission](https://github.com/MaKSiiMe/holbertonschool-hbnb/blob/main/Part1/2-%20Sequence_diagram_for_review_submission.md)  
    - [Fetching places](https://github.com/MaKSiiMe/holbertonschool-hbnb/blob/main/Part1/2-%20Sequence_diagram_for_fetching_a_list_of_places.md)  

---

### ⚙️ Part 2: Business Logic & API  
The **Business Logic (BL) Layer** and **API** are key components of the HBnB system, ensuring efficient handling of user requests and data processing. This section details how the business logic is structured and how the API provides a seamless interface for external interactions.  

#### 🔹 Business Logic Layer  
- Implements core functionalities such as **user authentication, property management, and review processing**.
- Uses **object-oriented programming (OOP)** principles to encapsulate logic and enforce data consistency.
- Interacts with the **database layer** to store and retrieve information efficiently.
- Implements error handling to ensure **data integrity** and **robust performance**.

#### 🔹 API Implementation  
- Built using **Flask** as a lightweight framework to handle HTTP requests and responses.
- Follows **RESTful principles**, making it scalable and easy to interact with.
- Provides **CRUD operations** for major entities such as **Users, Places, and Reviews**.
- Implements **JWT authentication** for secure access control.

#### 🌍 API Endpoints Overview  
| HTTP Method | Endpoint | Description |
|------------|---------|-------------|
| `GET` | `/api/v1/users` | Retrieve all users |
| `POST` | `/api/v1/users` | Create a new user |
| `GET` | `/api/v1/users/<user_id>` | Retrieve a specific user |
| `PUT` | `/api/v1/users/<user_id>` | Update user details |
| `DELETE` | `/api/v1/users/<user_id>` | Delete a user |
| `GET` | `/api/v1/places` | Retrieve all places |
| `POST` | `/api/v1/places` | Create a new place |
| `GET` | `/api/v1/places/<place_id>` | Retrieve a specific place |
| `PUT` | `/api/v1/places/<place_id>` | Update place details |
| `DELETE` | `/api/v1/places/<place_id>` | Delete a place |
| `GET` | `/api/v1/reviews` | Retrieve all reviews |
| `POST` | `/api/v1/reviews` | Submit a new review |
| `GET` | `/api/v1/reviews/<review_id>` | Retrieve a specific review |
| `PUT` | `/api/v1/reviews/<review_id>` | Update a review |
| `DELETE` | `/api/v1/reviews/<review_id>` | Delete a review |

---
>>>>>>> main

### 👤 Contributors:  
- [David Tolza](https://github.com/VidadTol)  
- [Giovanni Farias](https://github.com/ginftls)  
- [Ludiane Trouillefou](https://github.com/ludiane-tr)  
<<<<<<< HEAD
- [Maxime Truel](https://github.com/MaKSiiMe)  
=======
- [Maxime Truel](https://github.com/MaKSiiMe)
>>>>>>> main

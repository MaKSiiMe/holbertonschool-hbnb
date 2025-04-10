# <img src="https://cdn.prod.website-files.com/6105315644a26f77912a1ada/63eea844ae4e3022154e2878_Holberton-p-800.png" width="150" /> - HBNB Project - Cohort C#25  
The HBnB project at Holberton is a simplified full-stack clone of Airbnb. It covers various aspects of software development, including backend, database management, front-end integration, and deployment.

---
# HBnB Project - Part 3: Enhanced Backend with Authentication and Database Integration

Welcome to Part 3 of the HBnB project! In this section, you will enhance the backend of the application by integrating user authentication, implementing role-based authorization, and transitioning from in-memory storage to a relational database using SQLAlchemy and SQLite for development. Later, you'll configure MySQL for production environments. This part will set the foundation for a secure, scalable, and production-ready backend system.

## Objectives

### 1. **Authentication and Authorization:**
   - Implement JWT-based user authentication using **Flask-JWT-Extended**.
   - Implement role-based access control (RBAC) using the `is_admin` attribute for specific endpoints.

### 2. **Database Integration:**
   - Replace in-memory storage with **SQLite** for development using **SQLAlchemy** as the ORM.
   - Prepare the system for **MySQL** or other production-grade RDBMS.

### 3. **CRUD Operations with Database Persistence:**
   - Refactor all CRUD operations to interact with the new persistent database (SQLite during development, MySQL for production).

### 4. **Database Design and Visualization:**
   - Design and visualize the database schema using **mermaid.js**.
   - Ensure correct relationships between entities like Users, Places, Reviews, and Amenities.

### 5. **Data Consistency and Validation:**
   - Enforce data validation and constraints within the database models to ensure consistency.

---

## Structure of the Project

The tasks in this part of the project are organized progressively to help you build a complete, secure, and database-backed backend system:

1. **Modify the User Model to Include Password:**
   - Modify the User model to securely store passwords using **bcrypt2** and update the user registration process.

2. **Implement JWT Authentication:**
   - Secure the API by implementing JWT tokens. Only authenticated users should be able to access protected endpoints.

3. **Implement Authorization for Specific Endpoints:**
   - Implement role-based access control (RBAC) to restrict certain actions to administrators.

4. **SQLite Database Integration:**
   - Transition from in-memory storage to **SQLite** as the persistent database during development.

5. **Map Entities Using SQLAlchemy:**
   - Map existing entities (User, Place, Review, Amenity) to the database using **SQLAlchemy** and define relationships correctly.

6. **Prepare for MySQL in Production:**
   - Towards the end of this phase, configure the application to use **MySQL** in production environments while using **SQLite** for development.

7. **Database Design and Visualization:**
   - Use **mermaid.js** to create entity-relationship diagrams (ERDs) for the database schema and ensure all relationships are properly visualized.

---

## Final Deliverables

- A backend system with JWT-based authentication and role-based access control.
- A database-backed system with persistent storage using SQLite and preparation for MySQL deployment.
- A well-designed and visualized relational database schema.
- A secure, scalable, and production-ready backend ready for further enhancements.

---

### 👤 Contributors:  
- [David Tolza](https://github.com/VidadTol)  
- [Giovanni Farias](https://github.com/ginftls)  
- [Ludiane Trouillefou](https://github.com/ludiane-tr)  
- [Maxime Truel](https://github.com/MaKSiiMe)

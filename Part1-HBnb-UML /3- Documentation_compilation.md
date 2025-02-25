# HBnB Evolution - Technical Documentation

## 1. Context and Objective

This document serves as the foundation for the development of the HBnB Evolution application. It provides a comprehensive overview of the system’s architecture, business logic design, and interactions. The goal is to establish a well-structured and maintainable system before implementation.

## 2. Problem Description

HBnB Evolution is a simplified version of an AirBnB-like application that allows users to:

- **User Management:** Register, update profiles, and be classified as regular users or administrators.
- **Place Management:** List, modify, and delete properties with details such as name, description, price, and location.
- **Review Management:** Submit, update, and delete reviews including ratings and comments for places.
- **Amenity Management:** Manage amenities that can be associated with places.

## 3. Business Rules and Requirements

### User Entity

- Attributes: First name, last name, email, password.
- Identified as an administrator using a boolean attribute.
- Operations: Create, update, delete.

### Place Entity

- Attributes: Title, description, price, latitude, longitude.
- Associated with an owner (User entity).
- Can have a list of amenities.
- Operations: Create, update, delete, list.

### Review Entity

- Attributes: Rating, comment.
- Associated with a specific place and user.
- Operations: Create, update, delete, list by place.

### Amenity Entity

- Attributes: Name, description.
- Operations: Create, update, delete, list.

### Common Requirements

- Unique identification using UUID4.
- Audit fields: Creation and update timestamps.

## 4. Architecture and Layers

The application follows a **three-layer architecture**:

- **Presentation Layer:** Provides API services for user interaction.
- **Business Logic Layer:** Contains the core models and rules.
- **Persistence Layer:** Handles data storage and retrieval.

### High-Level Package Diagram

```mermaid
classDiagram
class PresentationLayer {
    <<Interface>>
    +FrontendServices
    +API
}
class BusinessLogicLayer {
    +BaseModel
    +UserModel
    +PlaceModel
    +ReviewsModel
    +AmenityModel
}
class PersistenceLayer {
    +DatabaseAccess
}
PresentationLayer --> BusinessLogicLayer : Facade Pattern
BusinessLogicLayer --> PersistenceLayer : Database Operations
```

## 5. Detailed Class Diagram for Business Logic Layer

### Key Entities and Relationships

- **User** → Creates **Places**, submits **Reviews**.
- **Place** → Associated with an **Owner (User)**, contains **Amenities**, receives **Reviews**.
- **Review** → Associated with a **User** and a **Place**.
- **Amenity** → Linked to **Places**.

### Class Diagram
```mermaid
classDiagram
    class BaseModel {
        + UUID4 id
        + datetime created_at
        + datetime updated_at
        + create()
        + update()
        + delete()
        }
    
    class User {
        + String firstName
        + String lastName
        + String email
        - String password
        - Boolean isAdmin
        }

    class Place {
        + String title
        + String description
        + Float price
        + Float latitude
        + Float longitude
        + list amenities
        + list_Places()
        }

    class Review {
        # UUID4 place_id
        # UUID4 user_id
        + Int rating
        + String comment
        }

    class Amenity {
        + String name
        + String description
        + list amenities()
        }

    BaseModel "1" <|-- "0..*" User
    BaseModel "1" <|-- "0..*" Place
    BaseModel "1" <|-- "0..*" Review
    BaseModel "1" <|-- "0..*" Amenity
    User "1" *-- "0..*" Place : creates
    User "1"  *-- "0..*" Review : writes
    Place "1" *-- "0..*" Review : receives
    Place "0..*" *-- "0..*" Amenity : has
```

## 6. Sequence Diagrams for API Calls

```mermaid
sequenceDiagram
    participant User
    participant Browser
    participant API
    participant BusinessLogic
    participant Database

    # User Registration: A user signs up for a new account.

    User->>Browser: Fill registration form
    Browser->>API: Send registration details
    API->>API: Validate and create user account
    API->>BusinessLogic: Validate and process request
    BusinessLogic->>Database: Check if user exists
    Database-->>BusinessLogic: User not found
    BusinessLogic->>Database: Store new user
    Database-->>BusinessLogic: Success
    BusinessLogic-->>API: Return response
    alt Success
        API-->>Browser: Return success message
        Browser-->>User: Display registration successful
    else Failure
        API-->>Browser: Return error message
        Browser-->>User: Display registration error
    end

    # Place Creation: A user creates a new place listing.

    User->>Browser: Fill place creation form
    Browser->>API: Send place details
    API->>BusinessLogic: Validate and process request
    BusinessLogic->>Database: Check if place exists
    Database-->>BusinessLogic: Place not found
    BusinessLogic->>Database: Store new place
    Database-->>BusinessLogic: Success
    BusinessLogic-->>API: Return response
    alt Success
        API-->>Browser: Return success message
        Browser-->>User: Display place creation successful
    else Failure
        API-->>Browser: Return error message
        Browser-->>User: Display place creation error
    end

    # Review Submission: A user submits a review for a place.

    User->>Browser: Submit review form
    Browser->>API: Send review details
    API->>BusinessLogic: Validate review data
    BusinessLogic->>Database: Check if place exists
    Database-->>BusinessLogic: Place found
    BusinessLogic->>Database: Store new review
    Database-->>BusinessLogic: Success
    BusinessLogic-->>API: Return success response
    API-->>Browser: Return review submitted message
    Browser-->>User: Display review confirmation

    # Fetching a List of Places: A user requests a list of places based on certain criteria.

    User->>Browser: Search for places
    Browser->>API: Request places list with filters
    API->>BusinessLogic: Retrieve places based on criteria
    BusinessLogic->>Database: Query places with filters
    Database-->>BusinessLogic: Return place list
    BusinessLogic-->>API: Return place list
    API-->>Browser: Return places list
    Browser-->>User: Display search results
```

### User Registration

```mermaid
sequenceDiagram
    participant User
    participant Browser
    participant API
    participant BusinessLogic
    participant Database

    # User Registration: A user signs up for a new account.

    User->>Browser: Fill registration form
    Browser->>API: Send registration details
    API->>API: Validate and create user account
    API->>BusinessLogic: Validate and process request
    BusinessLogic->>Database: Check if user exists
    Database-->>BusinessLogic: User not found
    BusinessLogic->>Database: Store new user
    Database-->>BusinessLogic: Success
    BusinessLogic-->>API: Return response
    alt Success
        API-->>Browser: Return success message
        Browser-->>User: Display registration successful
    else Failure
        API-->>Browser: Return error message
        Browser-->>User: Display registration error
    end
```

### Place Creation

```mermaid
sequenceDiagram
    participant User
    participant Browser
    participant API
    participant BusinessLogic
    participant Database

    # Place Creation: A user creates a new place listing.

    User->>Browser: Fill place creation form
    Browser->>API: Send place details
    API->>BusinessLogic: Validate and process request
    BusinessLogic->>Database: Check if place exists
    Database-->>BusinessLogic: Place not found
    BusinessLogic->>Database: Store new place
    Database-->>BusinessLogic: Success
    BusinessLogic-->>API: Return response
    alt Success
        API-->>Browser: Return success message
        Browser-->>User: Display place creation successful
    else Failure
        API-->>Browser: Return error message
        Browser-->>User: Display place creation error
    end
```

### Review Submission

```mermaid
sequenceDiagram
    participant User
    participant Browser
    participant API
    participant BusinessLogic
    participant Database

    # Review Submission: A user submits a review for a place.

    User->>Browser: Submit review form
    Browser->>API: Send review details
    API->>BusinessLogic: Validate review data
    BusinessLogic->>Database: Check if place exists
    Database-->>BusinessLogic: Place found
    BusinessLogic->>Database: Store new review
    Database-->>BusinessLogic: Success
    BusinessLogic-->>API: Return success response
    API-->>Browser: Return review submitted message
    Browser-->>User: Display review confirmation
```

### Fetching Places

```mermaid
sequenceDiagram
    participant User
    participant Browser
    participant API
    participant BusinessLogic
    participant Database

    # Fetching a List of Places: A user requests a list of places based on certain criteria.

    User->>Browser: Search for places
    Browser->>API: Request places list with filters
    API->>BusinessLogic: Retrieve places based on criteria
    BusinessLogic->>Database: Query places with filters
    Database-->>BusinessLogic: Return place list
    BusinessLogic-->>API: Return place list
    API-->>Browser: Return places list
    Browser-->>User: Display search results
```

## 7. Documentation Compilation

This document consolidates all diagrams and explanations to guide the next phase: implementation.

## 8. Conclusion

This technical documentation outlines the core design of the HBnB Evolution application, ensuring clarity in architecture, business logic, and system interactions before moving to the implementation phase.


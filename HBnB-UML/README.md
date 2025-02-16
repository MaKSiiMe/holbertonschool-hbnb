# 🏠 HBnB Project – Documentation  

## 📌 Introduction  

### 🎯 Objective  
This document provides a detailed plan for the **HBnB Evolution** application. It consolidates all diagrams and explanatory notes into a comprehensive technical reference, guiding the implementation phases and clarifying the system's architecture and design.  

### 📍 Project Scope  
**HBnB Evolution** is a simplified application inspired by Airbnb that allows users to:  
✔️ Register  
✔️ Add properties  
✔️ Associate amenities   
✔️ Submit reviews  

This documentation covers:  
📂 **General architecture** (package diagram)  
🛠 **Business model** (detailed class diagram)  
🔄 **API interactions** (sequence diagrams)  

---

## General Architecture  

### **Package Diagram**  
The architecture follows a **layered model**, integrating the **facade pattern** to simplify interactions between components.  

```mermaid
classDiagram
class PresentationLayer {
    <<Interface>>
    +FrontendServices
    +API
}
class BusinessLogicLayer {
    +User
    +Place
    +Reviews
    +Amenity

}
class PersistenceLayer {
    +DatabaseAccess
}
PresentationLayer --> BusinessLogicLayer : Facade Pattern
BusinessLogicLayer --> PersistenceLayer : Database Operations
```

**The 3 main layers**:  

1️⃣ **Presentation Layer**  
- Manages the user interface and interactions.  
- Receives requests and returns responses after processing.  

2️⃣ **Business Logic Layer**  
- Contains key models (**User, Place, Review, Amenity**).  
- Implements business rules and orchestrates operations.  
- Acts as a **facade** for communication with the persistence layer.  

3️⃣ **Persistence Layer**  
- Manages the database and CRUD operations.  
- Structures data to ensure integrity and consistency.  

## 🛠️ Business Logic Layer  


### 📌 **Class Diagram**  
The core of the application relies on several **key entities**:  

### High-Level Architecture - classDiagram
```mermaid
classDiagram
    class User {
        #UUID id
        +String firstName
        +String lastName
        +String email
        -String password
        -Boolean isAdmin
        +Date Creation
        +Date Updated
        +createUser()
        +updateUser()
        +deleteUser()
    }

    class Place {
        #UUID id
        +String title
        +String description
        +Float price
        +Float latitude
        +Float longitude
        +Date Creation
        +Date Updated
        +createPlace()
        +updatePlace()
        +deletePlace()
    }

    class Review {
        #UUID id
        +Int rating
        +String comment
        +Date Creation
        +Date Updated
        +createReview()
        +updateReview()
        +deleteReview()
    }

    class Amenity {
        #UUID id
        +String name
        +String description
        +Date Creation
        +Date Updated
        +createAmenity()
        +updateAmenity()
        +deleteAmenity()
    }

    User "1" -- "0..*" Place : owns
    User "1" -- "0..*" Review : submits
    Place "1" -- "0..*" Review : receives
    Place "1" -- "0..*" Amenity : has

```
### 🔗 **Entity Relationships**  
✔️ **A user** can own multiple **places** and leave multiple **reviews**.  
✔️ **A place** can receive multiple **reviews** and be associated with multiple **amenities**.  

The architecture of the business logic layer ensures **consistency, scalability, and modularity**.  

---
## 🔄 API Interaction Flow  

### 📊 **Sequence Diagrams for API calls**  
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

#### 📝 **1. User Registration**  
1️⃣ The user sends their information (**name, email, password**) to the **Presentation Layer**.  
2️⃣ It validates and forwards them to the **Business Logic Layer**.  
3️⃣ After validation, the data is stored via the **Persistence Layer**.  
4️⃣ A success or failure response is returned.  

#### 🏡 **2. Place Creation**  
1️⃣ The user submits a creation request (**title, description, etc.**).  
2️⃣ The **Presentation Layer** forwards the request to the **Business Logic Layer**.  
3️⃣ After validation, the data is inserted via the **Persistence Layer**.  
4️⃣ A confirmation is returned.  

#### ⭐ **3. Review Submission**  
1️⃣ The user wants to leave a review for a place.  
2️⃣ The **Presentation Layer** sends the details (**rating, comment, etc.**) to the **Business Logic Layer**.  
3️⃣ The review is stored via the **Persistence Layer**, and a response is returned.  

#### 📍 **4. Retrieving Available Places**  
1️⃣ The user requests the list of available places.  
2️⃣ The **Presentation Layer** queries the **Business Logic Layer**, which consults the **Persistence Layer**.  
3️⃣ The results are returned and displayed to the user.  

---

## 📌 Conclusion  

This document is a **comprehensive technical guide** for **HBnB Evolution**. It provides:  

📂 **An overview of the architecture** and the **facade pattern** 🏗️  
📊 **A structured business model** with a class diagram 🔍  
🔄 **A detailed API interaction schema** outlining the main operations  

🔹 **Readability and professionalism** ensure a clear understanding for developers throughout the implementation.  
🔹 This document will evolve to reflect project updates.  
